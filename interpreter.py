import importlib.util
import os.path

import codecs
import shlex
import sys

keywords = ['func', 'while', 'if', 'else', 'do', 'end', 'store', 'global', 'update', 'delete', 'return', 'break', 'continue', 'import']


def is_identifier(token, interpreter, allow_builtin=False) -> bool:
    if allow_builtin:
        return token.isidentifier() and token not in keywords
    else:
        return token.isidentifier() and token not in interpreter.builtins and token not in keywords


def lenlist(mylist):
    return *mylist, len(mylist)


def get_type(value) -> str:
    print(value, type(value))
    if isinstance(value, bool):
        return 'bool'
    if isinstance(value, str):
        return 'str'
    if isinstance(value, (int, float)):
        return 'float'
    if isinstance(value, Reference):
        return 'ref'
    if isinstance(value, Module):
        return 'module'
    if isinstance(value, list):
        return 'list'
    if isinstance(value, bytes):
        return 'bytes'
    raise TypeError(f'Invalid type {type(value)} for {value}')


def parse_value(token):
    if token in ['true', 'false']:
        return True if token == 'true' else False
    if (token.startswith('"') and token.endswith('"')) or (token.startswith('\'') and token.endswith('\'')):
        return codecs.decode(token[1:-1], 'unicode_escape')
    try:
        try:
            return int(token)
        except ValueError:
            return float(token)
    except ValueError:
        return None


def to_str(value, repr_=False) -> str:
    if isinstance(value, bool):
        if value:
            return 'true'
        else:
            return 'false'
    if isinstance(value, str):
        if repr_:
            return f'"{codecs.encode(value, "unicode_escape").decode("utf-8")}"'
        else:
            return value
    if isinstance(value, list):
        return f'['+', '.join([to_str(v, repr_=repr_) for v in value])+']'
    return str(value)


class Operation:
    def __init__(self, name):
        self.name = name

    def execute(self, interpreter: 'Interpreter'):
        raise NotImplemented

    def __repr__(self):
        return f'{type(self).__name__}[name="{self.name}"]'


class Builtin(Operation):
    def __init__(self, name, value_count: int, func):
        super().__init__(name)
        self.value_count = value_count
        self.func = func

    def execute(self, interpreter: 'Interpreter'):
        self.func(interpreter, *interpreter.pop_stack(self.value_count))


class Import(Operation):
    def execute(self, interpreter: 'Interpreter'):
        module: str = interpreter.pop_stack(1)[0]
        parts = module.split('.')
        path = 'lib/'+'/'.join(parts)
        if os.path.isfile(path + '.st'):  # "std.test" import store test
            path += '.st'
            importer = Interpreter()
            M = Module(module, None)
            importer.global_scope.module = M
            with open(path, 'r') as file:
                importer.parse(file.read())
            importer.execute_all()
            M.funcs = importer.layers[0]
            d = []
            for key, func in M.funcs.items():
                if isinstance(func, Variable):
                    if func.is_global:
                        interpreter.layers[0][key] = func
                        d.append(key)
            for k in d:
                del M.funcs[k]
            interpreter.stack.append(M)
            return
        elif os.path.isfile(path + '.st.py'):  # "std.math" import store math
            path += '.st.py'
            spec = importlib.util.spec_from_file_location("module.name", path)
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            assert hasattr(m, 'export'), f'python based module {module} misses function "export"'
            funcs: dict = m.export()
            M = Module(module, funcs)
            d = []
            for key, func in M.funcs.items():
                if isinstance(func, Scope):
                    func.module = M
                if isinstance(func, Variable):
                    if func.is_global:
                        interpreter.layers[0][key] = func
                        d.append(key)
            for k in d:
                del M.funcs[k]
            interpreter.stack.append(M)
            return
        raise RuntimeException(f'module "{module}" can not be found')


class PushValue(Operation):
    def __init__(self, name, value, onpush=lambda v, i: ()):
        super().__init__(name)
        self.value = value
        self.onpush = onpush

    def execute(self, interpreter: 'Interpreter'):
        self.onpush(self.value, interpreter)
        interpreter.stack.append(self.value)


class DeclareFunction(Operation):
    def __init__(self, name, function: 'Function'):
        super().__init__(name)
        self.function = function

    def execute(self, interpreter: 'Interpreter'):
        interpreter.layers[-1][self.name] = self.function


class StoreVariable(Operation):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, interpreter: 'Interpreter'):
        interpreter.layers[-1][self.name] = Variable(self.name, interpreter.pop_stack(1)[0])


class GlobalVariable(Operation):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, interpreter: 'Interpreter'):
        v = Variable(self.name, interpreter.pop_stack(1)[0])
        v.is_global = True
        interpreter.layers[0][self.name] = v


class UpdateVariable(Operation):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, interpreter: 'Interpreter'):
        if interpreter.scope_stack[-1].scope.module is not None:  # the to be updated variable may be part of module
            if self.name in interpreter.scope_stack[-1].scope.module.funcs:
                interpreter.scope_stack[-1].scope.module.funcs[self.name].value = interpreter.pop_stack(1)[0]
                return
        for i in range(len(interpreter.layers) - 1, -1, -1):
            if self.name in interpreter.layers[i]:
                interpreter.layers[i][self.name].value = interpreter.pop_stack(1)[0]
                return
        raise RuntimeException(f'Variable "{self.name}" does not seem to exist and therefore cannot be updated')


class DeleteVariableOrFunc(Operation):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, interpreter: 'Interpreter'):
        if interpreter.scope_stack[-1].scope.module is not None:  # the to be updated variable may be part of module
            if self.name in interpreter.scope_stack[-1].scope.module.funcs:
                del interpreter.scope_stack[-1].scope.module.funcs[self.name]
                return
        for i in range(len(interpreter.layers) - 1, -1, -1):
            if self.name in interpreter.layers[i]:
                del interpreter.layers[i][self.name]
                return
        raise RuntimeException(f'Identifier "{self.name}" does not seem to exist and therefore cannot be deleted')


class Call(Operation):
    def execute(self, interpreter: 'Interpreter'):
        if interpreter.scope_stack[-1].scope.module is not None:  # the to be updated variable may be part of module
            if interpreter.scope_stack[-1].scope.module.funcs is not None:  # called during import: nope, not good
                if self.name in interpreter.scope_stack[-1].scope.module.funcs:
                    call = interpreter.scope_stack[-1].scope.module.funcs[self.name]
                    if isinstance(call, Function):
                        interpreter.scope_stack.append(call.start(interpreter))
                        return
                    if isinstance(call, Variable):
                        interpreter.stack.append(call.value)
                        return
                    raise RuntimeException(f'Invalid call type "{type(call).__name__}"')
        for layer in reversed(interpreter.layers):
            if self.name in layer:
                call = layer[self.name]
                if isinstance(call, Function):
                    interpreter.scope_stack.append(call.start(interpreter))
                    return
                if isinstance(call, Variable):
                    interpreter.stack.append(call.value)
                    return
                raise RuntimeException(f'Invalid call type "{type(call).__name__}"')
        raise RuntimeException(f'"{self.name}" could not be found as a valid function or variable')


class CallIf(Operation):
    def __init__(self, name, scope: 'Scope'):
        super().__init__(name)
        self.scope = scope

    def execute(self, interpreter: 'Interpreter'):
        is_true = interpreter.pop_stack(1)[0] == True  # == True is important else it will let almost anything be True
        if interpreter.scope_stack[-1].has_next():
            potential_else = interpreter.scope_stack[-1].scope.operations[interpreter.scope_stack[-1].pointer]
            if isinstance(potential_else, CallElse):
                interpreter.scope_stack[-1].pointer += 1
                if not is_true:
                    potential_else.execute(interpreter, after_if=True)
            if is_true:
                interpreter.scope_stack.append(self.scope.start(interpreter))


class CallElse(Operation):
    def __init__(self, name, scope: 'Scope'):
        super().__init__(name)
        self.scope = scope

    def execute(self, interpreter: 'Interpreter', after_if=False):  # after if ensures it is called after an if and not randomly
        assert after_if, 'this "else" was not proceeded by an "if"'
        interpreter.scope_stack.append(self.scope.start(interpreter))


class CallWhile(Operation):
    def __init__(self, name, scope: 'Scope'):
        super().__init__(name)
        self.scope = scope

    def execute(self, interpreter: 'Interpreter'):
        if interpreter.pop_stack(1)[0] == True:  # == True is important else it will let almost anything be True
            interpreter.scope_stack[-1].pointer -= 1
            interpreter.scope_stack.append(self.scope.start(interpreter))


class EndScope(Operation):
    def execute(self, interpreter: 'Interpreter'):
        interpreter.layers.pop()
        interpreter.scope_stack.pop()


class Return(Operation):
    def execute(self, interpreter: 'Interpreter'):
        interpreter.layers.pop()
        popped = interpreter.scope_stack.pop()
        while not isinstance(popped.scope, Function):
            interpreter.layers.pop()
            popped = interpreter.scope_stack.pop()
        else:
            raise RuntimeException('"Can not use "return" outside of "function"')


class Break(Operation):
    def execute(self, interpreter: 'Interpreter'):
        interpreter.layers.pop()
        popped = interpreter.scope_stack.pop()
        while not isinstance(popped.scope, While):
            interpreter.layers.pop()
            popped = interpreter.scope_stack.pop()
            interpreter.scope_stack[-1].pointer += 1
        else:
            raise RuntimeException('"Can not use "break" outside of "while"')


class Continue(Operation):
    def execute(self, interpreter: 'Interpreter'):
        interpreter.layers.pop()
        popped = interpreter.scope_stack.pop()
        while not isinstance(popped.scope, While):
            interpreter.layers.pop()
            popped = interpreter.scope_stack.pop()
        else:
            raise RuntimeException('"Can not use "continue" outside of "while"')


class ParseException(Exception):
    pass


class RuntimeException(Exception):
    pass


class ParseReturn(Exception):
    pass


class Scope:
    def __init__(self, name, interpreter: 'Interpreter'):
        self.name = name
        self.operations: list[Operation] = []
        self.inner_scope_status: str = ''
        self.inner_scope: Function = None
        self.module: Module = None  # will set upon import if this scope is part of a module

    def add_token(self, token: str, interpreter: 'Interpreter'):
        if self.inner_scope_status != '':
            if self.inner_scope_status in ['store', 'global', 'update', 'delete']:
                if is_identifier(token, interpreter):
                    if self.inner_scope_status == ['delete', 'update']:
                        self.operations.append(DeleteVariableOrFunc(token))
                        self.inner_scope_status = ''
                        interpreter.tokening_indent -= 1
                        interpreter.console_prefix = '#'
                        return
                    if self.inner_scope_status in ['store', 'global']:
                        if self.inner_scope_status == 'store':
                            self.operations.append(StoreVariable(token))
                        if self.inner_scope_status == 'global':
                            self.operations.append(GlobalVariable(token))
                    else:
                        self.operations.append(UpdateVariable(token))
                    self.inner_scope_status = ''
                    interpreter.tokening_indent -= 1
                    interpreter.console_prefix = '#'
                    return
                self.inner_scope_status = ''
                interpreter.tokening_indent -= 1
                interpreter.console_prefix = '#'
                raise ParseException(f'"{token}" is not a valid identifier '
                                     f'{"(Can not override builtins)" if token in interpreter.builtins else ""}')
            if self.inner_scope_status == 'func':
                if is_identifier(token, interpreter):
                    self.inner_scope = Function(token, interpreter)
                    self.inner_scope.module = self.module
                    self.inner_scope_status += '.do'
                    interpreter.console_prefix = '.'
                    return
                self.inner_scope_status = ''
                interpreter.tokening_indent -= 1
                interpreter.console_prefix = '#'
                raise ParseException(f'"{token}" is not a valid identifier '
                                     f'{"(Can not override builtins)" if token in interpreter.builtins else ""}')
            if self.inner_scope_status.endswith('.do'):
                if token == 'do':
                    self.inner_scope_status += '.scope'
                    interpreter.console_prefix = '#'
                    return
                self.inner_scope_status = ''
                self.inner_scope = None
                interpreter.tokening_indent -= 1
                interpreter.console_prefix = '#'
                raise ParseException(f'Expected "do" got "{token}"')
            if self.inner_scope_status.endswith('.scope'):
                try:
                    self.inner_scope.add_token(token, interpreter)
                except ParseReturn:
                    self.inner_scope.operations.append(EndScope(token))
                    if self.inner_scope_status.startswith('func'):
                        self.operations.append(DeclareFunction(self.inner_scope.name, self.inner_scope))
                    elif self.inner_scope_status.startswith('if'):
                        self.operations.append(CallIf(self.inner_scope.name, self.inner_scope))
                    elif self.inner_scope_status.startswith('else'):
                        self.operations.append(CallElse(self.inner_scope.name, self.inner_scope))
                    elif self.inner_scope_status.startswith('while'):
                        self.operations.append(CallWhile(self.inner_scope.name, self.inner_scope))
                    self.inner_scope_status = ''
                    interpreter.tokening_indent -= 1
                    interpreter.console_prefix = '#'
                    self.inner_scope = None
                return
            raise ParseException(f'Error with token "{token}" during {self.inner_scope_status} creation')
        if token.startswith('@') and len(token) > 1:
            if token[1:].startswith(':'):
                moduled = lambda v, i: v.register_module(interpreter)
                token = token[1:]
            else:
                moduled = lambda v, i: ()
            if is_identifier(token[1:], interpreter, allow_builtin=True) or token[1:] in interpreter.builtins:
                self.operations.append(PushValue(token, Reference(token[1:]), onpush=moduled))
                return
            else:
                raise ParseException(f'"{token}" is not a valid identifier')
        if token.startswith(':') and len(token) > 1:
            self.operations.append(ModuleFunc(token, token[1:]))
            return
        if token in ['func', 'store', 'global', 'update', 'delete']:
            interpreter.tokening_indent += 1
            self.inner_scope_status = token
            interpreter.console_prefix = '+'
            return
        if token in ['if', 'elif', 'else', 'while']:
            interpreter.tokening_indent += 1
            self.inner_scope_status = token + '.scope'
            if token == 'if':
                self.inner_scope = If(token, interpreter)
                self.inner_scope.module = self.module
            if token == 'else':
                self.inner_scope = Else(token, interpreter)
                self.inner_scope.module = self.module
            if token == 'while':
                self.inner_scope = While(token, interpreter)
                self.inner_scope.module = self.module
            return
        if token in ['return', 'break', 'continue']:
            if token == 'return':
                self.operations.append(Return(token))
            if token == 'break':
                self.operations.append(Break(token))
            if token == 'continue':
                self.operations.append(Continue(token))
            return
        v = parse_value(token)
        if v is not None:
            self.operations.append(PushValue(token, v))
            return
        if token in interpreter.builtins:
            self.operations.append(interpreter.builtins[token])
            return
        if is_identifier(token, interpreter):
            self.operations.append(Call(token))
            return
        if token == 'end':
            raise ParseReturn
        raise ParseException(f'Invalid token "{token}"')

    def start(self, interpreter: 'Interpreter') -> 'ScopeExecutioner':
        interpreter.layers.append({})
        return ScopeExecutioner(self)

    def __repr__(self):
        return f'{type(self).__name__}[name="{self.name}"{f" in {self.module}" if self.module is not None else ""}, ops={len(self.operations)}]'


class ScopeExecutioner:
    def __init__(self, scope: Scope):
        self.scope = scope
        self.pointer = 0

    def get_next(self) -> Operation:
        assert self.has_next(), 'No more tokens to execute'
        self.pointer += 1
        return self.scope.operations[self.pointer - 1]

    def has_next(self) -> bool:
        return self.pointer < len(self.scope.operations)

    def trace(self) -> str:
        return f'{self.scope.name}[{self.pointer}]'

    def __repr__(self):
        return f'{f"{self.scope.module.name} :" if self.scope.module is not None else ""}{self.scope.name}[pointer={self.pointer}, ops={len(self.scope.operations)}]'


class Function(Scope):
    ...


class If(Scope):
    ...


class Else(Scope):
    ...


class While(Scope):
    ...


class Variable:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.is_global = False

    def __repr__(self):
        return f'Variable[name="{self.name}", value={to_str(self.value, repr_=True)}]'


class Module:
    def __init__(self, name, funcs):
        self.name = name
        self.funcs: dict = funcs

    def __repr__(self):
        return f'{self.name}'


class ModuleFunc(Operation):
    def __init__(self, name, operation):
        super().__init__(name)
        self.operation = operation

    def execute(self, interpreter: "Interpreter"):
        module = interpreter.pop_stack(1)[0]
        assert isinstance(module, Module), f'"{module}" is not a module'
        assert self.operation in module.funcs, \
            f'module "{module.name}" does not have an attribute "{self.operation}"'
        call = module.funcs[self.operation]
        if isinstance(call, Function):
            interpreter.scope_stack.append(call.start(interpreter))
            return
        if isinstance(call, Operation):
            call.execute(interpreter)
            return
        if isinstance(call, Variable):
            interpreter.stack.append(call.value)
            return


class Reference:
    def __init__(self, ref_to):
        self.ref_to = ref_to
        self.module: Module = None

    def register_module(self, interpreter: 'Interpreter'):
        self.module = interpreter.pop_stack(1)[0]
        assert isinstance(self.module, Module), f'"{self.module}" is not a module'

    def call(self, interpreter: 'Interpreter'):
        if self.module is not None:
            call = self.module.funcs[self.ref_to]
        elif self.ref_to in interpreter.builtins:
            call = interpreter.builtins[self.ref_to]
        else:
            for layer in reversed(interpreter.layers):
                if self.ref_to in layer:
                    call = layer[self.ref_to]
                    break
            else:
                raise RuntimeException(f'"{self.ref_to}" could not be found as a valid function or variable')

        if isinstance(call, Function):
            interpreter.scope_stack.append(call.start(interpreter))
            return
        if isinstance(call, Operation):
            call.execute(interpreter)
            return
        if isinstance(call, Variable):
            interpreter.stack.append(call.value)
            return
        raise RuntimeException(f'Invalid call type {type(call)}')

    def __repr__(self):
        return f'{f"{self.module} @:" if self.module is not None else "@"}{self.ref_to}'


class Global(Scope):
    ...


class Interpreter:
    def __init__(self):
        self.tokening_indent = 0
        self.stack = [*sys.argv]
        self.layers: list[dict] = []
        self.scope_stack: list[ScopeExecutioner] = []
        self.console_prefix = '#'

        spec = importlib.util.spec_from_file_location("module.name", 'lib/std/builtins.st.py')
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        self.builtins: dict[str, Builtin] = m.export()

        self.global_scope = Global('global', self)
        self.scope_stack.append(self.global_scope.start(self))

    def add_token(self, code: str):
        try:
            self.global_scope.add_token(code, self)
        except ParseReturn:
            raise ParseException(f'Cannot end {self.global_scope.name}')

    def execute(self, debug=False, cmd=False):
        try:
            operation: Operation = self.scope_stack[-1].get_next()
            operation.execute(self)
            if debug:
                print(f'operation = {operation}')
                print(f'scope_stack = {self.scope_stack}')
                print(f'trace = {self.trace()}')
                print(f'layers = {self.layers}')
                print(f'stack = {self.stack}')
                print()
        except BaseException:
            if not cmd:
                print(f'Error in op "{operation.name}": {self.trace()}')
            raise

    def execute_all(self, debug=False, cmd=False):
        while self.scope_stack[-1].has_next():
            self.execute(debug=debug, cmd=cmd)

    def parse(self, script: str):
        for line in script.split('\n'):
            self.parse_line(line)

    def parse_line(self, line: str):
        tokens = shlex.split(line, posix=False)
        for token in tokens:
            if token.startswith('//'):
                break
            self.add_token(token)

    def run_repl(self, stack_max=16, debug=False):
        while True:
            try:
                try:
                    print(self.console_prefix + ('..' * self.tokening_indent) + ' ', end='')
                    inp = input()
                    self.parse_line(inp)
                    self.execute_all(debug=debug, cmd=True)
                except (AssertionError, TypeError, ParseException, RuntimeException) as e:
                    sys.stderr.write(str(e) + '\n')
                    sys.stderr.flush()
                    print('', end='')

                if stack_max > 0 and self.tokening_indent == 0:
                    print(f'[{"..., " if len(self.stack) > stack_max else ""}'
                          f'{", ".join(to_str(v, repr_=True) for v in self.stack[-stack_max:])}]')
            except KeyboardInterrupt:
                self.layers = [self.layers[0]]
                self.tokening_indent = 0
                self.console_prefix = '#'
                self.global_scope = Global('global', self)
                self.scope_stack = [self.global_scope.start(self)]
                sys.stderr.write('Crtl+C\n')
                sys.stderr.flush()
                print('', end='')

    def pop_stack(self, values) -> list:
        assert len(self.stack) >= values, f'Stack has not enough values (found {len(self.stack)}, expected {values})'
        assert values >= 0, 'Can only pop an amount of values >= 0'
        if values == 0:
            return []
        if values == 1:
            return [self.stack.pop()]
        # self.stack, v = self.stack[:-values], self.stack[-values:]
        return list(reversed([self.stack.pop() for _ in range(values)]))

    def trace(self) -> str:
        return ' in '.join(f'{f"{f.scope.module.name} :" if f.scope.module is not None else ""}{f.scope.name}<{type(f.scope).__name__}>{f.pointer}' for f in reversed(self.scope_stack))