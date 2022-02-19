import codecs
import shlex
import sys


def is_identifier(token, interpreter, allow_builtin=False) -> bool:
    if allow_builtin:
        return token.isidentifier() and token not in ['func', 'while', 'if', 'do', 'end']
    else:
        return token.isidentifier() and token not in interpreter.builtins and token not in ['func', 'while', 'if', 'do',
                                                                                            'end']


def get_type(value) -> str:
    print(value, type(value))
    if isinstance(value, bool):
        return 'bool'
    if isinstance(value, str):
        return 'str'
    if isinstance(value, (int, float)):
        return 'float'


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
    return str(value)


class Operation:
    def __init__(self, name):
        self.name = name

    # def get_location(self) -> str:
    #     return f'token {self.token_nr} "{self.token_label}" in file {self.file} in line {self.line}'

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
        self.func(*interpreter.pop_stack(self.value_count))


class PushValue(Operation):
    def __init__(self, name, value):
        super().__init__(name)
        self.value = value

    def execute(self, interpreter: 'Interpreter'):
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


class UpdateVariable(Operation):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, interpreter: 'Interpreter'):
        for i in range(len(interpreter.layers) - 1, -1, -1):
            if self.name in interpreter.layers[i]:
                interpreter.layers[i][self.name].value = interpreter.pop_stack(1)[0]
                return
        raise RuntimeException(f'Variable "{self.name}" does not seem to exist and therefore cannot be updated')


class DeleteVariableOrFunc(Operation):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, interpreter: 'Interpreter'):
        for i in range(len(interpreter.layers) - 1, -1, -1):
            if self.name in interpreter.layers[i]:
                del interpreter.layers[i][self.name]
                return
        raise RuntimeException(f'Identifier "{self.name}" does not seem to exist and therefore cannot be deleted')


class Call(Operation):
    def execute(self, interpreter: 'Interpreter'):
        for layer in reversed(interpreter.layers):
            if self.name in layer:
                call = layer[self.name]
                if isinstance(call, Function):
                    interpreter.scope_stack.append(call.start(interpreter))
                    return
                if isinstance(call, Variable):
                    interpreter.stack.append(call.value)
                    return
                raise RuntimeException(f'Invalid call type {type(call)}')
        raise RuntimeException(f'"{self.name}" could not be found as a valid function or variable')


class CallIf(Operation):
    def __init__(self, name, scope: 'Scope'):
        super().__init__(name)
        self.scope = scope

    def execute(self, interpreter: 'Interpreter'):
        if interpreter.pop_stack(1)[0] == True:  # == True is important else it will let almost anything be True
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


class ParseException(Exception):
    pass


class RuntimeException(Exception):
    pass


class Return(Exception):
    pass


class Scope:
    def __init__(self, name, interpreter: 'Interpreter'):
        self.name = name
        self.operations: list[Operation] = []
        self.inner_scope_status: str = ''
        self.inner_scope: Function = None
        interpreter.parse_time_func_var_stack.append([])

    def add_token(self, token: str, interpreter: 'Interpreter'):
        if self.inner_scope_status != '':
            if self.inner_scope_status in ['store', 'update', 'delete']:
                if is_identifier(token, interpreter):
                    if self.inner_scope_status == 'delete':
                        for ptfvs in interpreter.parse_time_func_var_stack:
                            if token in ptfvs:
                                self.operations.append(DeleteVariableOrFunc(token))
                                self.inner_scope_status = ''
                                interpreter.tokening_indent -= 1
                                interpreter.console_prefix = '#'
                                return
                        self.inner_scope_status = ''
                        interpreter.tokening_indent -= 1
                        interpreter.console_prefix = '#'
                        raise ParseException(f'"{token}" is not an existing identifier and therefore can not be deleted')
                    if self.inner_scope_status == 'update':
                        for ptfvs in interpreter.parse_time_func_var_stack:
                            if token in ptfvs:
                                break
                        else:
                            self.inner_scope_status = ''
                            interpreter.tokening_indent -= 1
                            interpreter.console_prefix = '#'
                            raise ParseException(f'"{token}" is not an existing identifier and therefore can not be updated')
                    if self.inner_scope_status == 'store':
                        self.operations.append(StoreVariable(token))
                        interpreter.parse_time_func_var_stack[-1].append(token)
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
                except Return:
                    self.inner_scope.operations.append(EndScope(token))
                    if self.inner_scope_status.startswith('func'):
                        interpreter.parse_time_func_var_stack[-1].append(self.inner_scope.name)
                        self.operations.append(DeclareFunction(self.inner_scope.name, self.inner_scope))
                    elif self.inner_scope_status.startswith('if'):
                        self.operations.append(CallIf(self.inner_scope.name, self.inner_scope))
                    elif self.inner_scope_status.startswith('while'):
                        self.operations.append(CallWhile(self.inner_scope.name, self.inner_scope))
                    self.inner_scope_status = ''
                    interpreter.tokening_indent -= 1
                    interpreter.console_prefix = '#'
                    self.inner_scope = None
                return
            raise ParseException(f'Error with token "{token}" during {self.inner_scope_status} creation')
        if token.startswith('@') and len(token) > 1:
            if is_identifier(token[1:], interpreter, allow_builtin=True) or token[1:] in interpreter.builtins:
                self.operations.append(PushValue(token, Reference(token[1:])))
                return
            else:
                raise ParseException(f'"{token}" is not a valid identifier')
        if token in ['func', 'store', 'update', 'delete']:
            interpreter.tokening_indent += 1
            self.inner_scope_status = token
            interpreter.console_prefix = '+'
            return
        if token in ['if', 'while']:
            interpreter.tokening_indent += 1
            self.inner_scope_status = token + '.scope'
            if token == 'if':
                self.inner_scope = If(token, interpreter)
            if token == 'while':
                self.inner_scope = While(token, interpreter)
            return
        v = parse_value(token)
        if v is not None:
            self.operations.append(PushValue(token, v))
            return
        if token in interpreter.builtins:
            self.operations.append(interpreter.builtins[token])
            return
        if is_identifier(token, interpreter):
            for ptfvs in interpreter.parse_time_func_var_stack:
                if token in ptfvs:
                    self.operations.append(Call(token))
                    return
        if token == 'end':
            interpreter.parse_time_func_var_stack.pop()
            raise Return
        raise ParseException(f'Invalid token "{token}"')

    def start(self, interpreter: 'Interpreter') -> 'ScopeExecutioner':
        interpreter.layers.append({})
        return ScopeExecutioner(self)

    def __repr__(self):
        return f'{type(self).__name__}[name="{self.name}", ops={len(self.operations)}]'


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
        return f'{self.scope.name}[pointer={self.pointer}, ops={len(self.scope.operations)}]'


class Function(Scope):
    ...


class If(Scope):
    ...


class While(Scope):
    ...


class Variable:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f'Variable[name="{self.name}", value={to_str(self.value, repr_=True)}]'


class Reference:
    def __init__(self, ref_to):
        self.ref_to = ref_to

    def call(self, interpreter: 'Interpreter'):
        if self.ref_to in interpreter.builtins:
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
        if isinstance(call, Builtin):
            call.execute(interpreter)
            return
        if isinstance(call, Variable):
            interpreter.stack.append(call.value)
            return
        raise RuntimeException(f'Invalid call type {type(call)}')

    def __repr__(self):
        return f'@{self.ref_to}'


class Global(Scope):
    ...


class Interpreter:
    def __init__(self):
        self.tokening_indent = 0
        self.stack = []
        self.layers: list[dict] = []
        self.parse_time_func_var_stack: list[list[str]] = []
        self.scope_stack: list[ScopeExecutioner] = []
        self.console_prefix = '#'

        def call_ref(v):
            try:
                v.call(self)
            except AttributeError:
                raise TypeError(f'"{v}" is not a reference')
        self.builtins: dict[str, Builtin] = {
            'clear': Builtin('clear', 0, lambda: self.stack.clear()),
            'dump': Builtin('dump', 0, lambda: self.stack.append(f'[{", ".join(to_str(v, repr_=True) for v in self.stack)}]')),
            'trace': Builtin('trace', 0, lambda: self.stack.append(self.trace())),
            'stacklen': Builtin('stacklen', 0, lambda: self.stack.append(len(self.stack))),

            '~': Builtin('~', 1, lambda v: self.stack.append(~v)),
            '!': Builtin('!', 1, lambda v: self.stack.append(True if v == 0 else False)),
            '@': Builtin('@', 1, lambda v: call_ref(v)),
            'out': Builtin('out', 1, lambda v: print(to_str(v), end='')),
            'outln': Builtin('outln', 1, lambda v: print(v)),
            'in': Builtin('in', 1, lambda v: self.stack.append(input(v))),
            'sqrt': Builtin('in', 1, lambda v: self.stack.append(input(v))),
            'parse': Builtin('parse', 1, lambda v: self.stack.append(parse_value(v))),
            'dup': Builtin('dup', 1, lambda v: self.stack.extend((v, v))),
            'rem': Builtin('rem', 0, lambda v: [self.stack.pop() for _ in range(v)]),
            'num': Builtin('num', 1, lambda v: self.stack.append(float(v))),
            'bool': Builtin('bool', 1, lambda v: self.stack.append(True if v == 'true' else False)),
            'type': Builtin('type', 1, lambda v: get_type(v)),
            'str': Builtin('str', 1, lambda v: self.stack.append(to_str(v))),
            'chr': Builtin('str', 1, lambda v: self.stack.append(ord(v))),
            'ord': Builtin('str', 1, lambda v: self.stack.append(chr(v))),
            'pull': Builtin('pull', 1, lambda v: self.stack.append(self.stack.pop(-v))),
            'drop': Builtin('drop', 1, lambda v: ()),

            '+': Builtin('+', 2, lambda b, a: self.stack.append(a + b)),
            '-': Builtin('-', 2, lambda b, a: self.stack.append(a - b)),
            '*': Builtin('*', 2, lambda b, a: self.stack.append(a * b)),
            '/': Builtin('/', 2, lambda b, a: self.stack.append(a / b)),
            '**': Builtin('**', 2, lambda b, a: self.stack.append(a ** b)),
            '%': Builtin('%', 2, lambda b, a: self.stack.append(a % b)),
            '|': Builtin('|', 2, lambda b, a: self.stack.append(a | b)),
            '^': Builtin('^', 2, lambda b, a: self.stack.append(a ^ b)),
            '&': Builtin('&', 2, lambda b, a: self.stack.append(a & b)),
            '>>': Builtin('>>', 2, lambda b, a: self.stack.append(a >> b)),
            '<<': Builtin('<<', 2, lambda b, a: self.stack.append(a << b)),
            '=': Builtin('=', 2, lambda b, a: self.stack.append(a == b)),
            '>': Builtin('>', 2, lambda b, a: self.stack.append(a > b)),
            '<': Builtin('<', 2, lambda b, a: self.stack.append(a < b)),
            '>=': Builtin('>=', 2, lambda b, a: self.stack.append(a >= b)),
            '<=': Builtin('<=', 2, lambda b, a: self.stack.append(a <= b)),
            'swap': Builtin('swap', 2, lambda b, a: self.stack.extend((b, a))),
            'push': Builtin('push', 2, lambda b, a: self.stack.insert(-b, a)),  # dest, obj
            'chrat': Builtin('chrat', 2, lambda b, a: self.stack.append(a[b])),
            'split': Builtin('split', 2, lambda b, a: self.stack.extend((a[:b], a[b:]))),

            'sth': Builtin('sth', 3, lambda c, b, a: self.stack.extend((c, a, b))),  # a b c -> c b a
        }

        self.global_scope = Global('global', self)
        self.scope_stack.append(self.global_scope.start(self))

    def add_token(self, code: str):
        try:
            self.global_scope.add_token(code, self)
        except Return:
            raise ParseException(f'Cannot end {self.global_scope.name}')

    def execute(self, debug=False):
        operation: Operation = self.scope_stack[-1].get_next()
        operation.execute(self)
        if debug:
            print(f'operation = {operation}')
            print(f'scope_stack = {self.scope_stack}')
            print(f'layers = {self.layers}')
            print(f'builtins = {self.builtins}')

    def execute_all(self, debug=False):
        while self.scope_stack[-1].has_next():
            self.execute(debug=debug)

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
                    self.execute_all(debug=debug)
                except (AssertionError, TypeError, ParseException, RuntimeException) as e:
                    sys.stderr.write(str(e) + '\n')
                    sys.stderr.flush()
                    print('', end='')

                if stack_max > 0 and self.tokening_indent == 0:
                    print(f'[{"..., " if len(self.stack) > stack_max else ""}'
                          f'{", ".join(to_str(v, repr_=True) for v in self.stack[-stack_max:])}]')
            except KeyboardInterrupt:
                self.layers = [self.layers[0]]
                self.parse_time_func_var_stack = [self.parse_time_func_var_stack[0]]
                self.tokening_indent = 0
                self.console_prefix = '#'
                self.global_scope = Global('global', self)
                self.scope_stack = [self.global_scope.start(self)]
                sys.stderr.write('Crtl+C\n')
                sys.stderr.flush()
                print('', end='')

    def pop_stack(self, values):
        assert len(self.stack) >= values, f'Stack has not enough values (found {len(self.stack)}, expected {values})'
        return [self.stack.pop() for _ in range(values)]

    def trace(self) -> str:
        return ' in '.join(f'{f.scope.name}<{type(f.scope).__name__}>{f.pointer}' for f in reversed(self.scope_stack))