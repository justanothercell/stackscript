import codecs


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


class Builtin(Operation):
    def __init__(self, name, value_count: int, func):
        super().__init__(name)
        self.value_count = value_count
        self.func = func

    def execute(self, interpreter: 'Interpreter'):
        self.func(*interpreter.pop_stack(self.value_count))


class StackAddValue(Operation):
    def __init__(self, name, value):
        super().__init__(name)
        self.value = value

    def execute(self, interpreter: 'Interpreter'):
        interpreter.stack.append(self.value)


class InvalidToken(Exception):
    pass


class Scope:
    def __init__(self, name):
        self.name = name
        self.operations: list[Operation] = []

    def add_token(self, token: str, interpreter: 'Interpreter'):
        v = parse_value(token)
        if v is not None:
            self.operations.append(StackAddValue(token, v))
            return
        if token in interpreter.builtins:
            self.operations.append(interpreter.builtins[token])
            return
        raise InvalidToken(token)

    def start(self) -> 'ScopeExecutioner':
        return ScopeExecutioner(self)


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

    def exec_next(self) -> bool:  # returns true when return from func
        assert len(self.func.operations) >= self.pointer, 'Function ended without receiving proper end!'
        code = self.func.operations[self.pointer]
        self.pointer += 1
        if self.status != '':
            if self.status == 'func':
                if code.isidentifier() and code not in self.interpreter.builtins:
                    self.status = 'func.named'
                    self.func_build = Function(code, self.interpreter)
                    return False
                self.status = ''
                raise Exception(f'Invalid name "{code}" for function. Cannot use names of builtins!')
            if self.status == 'func.named':
                if code == 'do':
                    self.status = 'func.body'
                    self.interpreter.layer += 1
                    return False
                self.func_build = None
                self.status = ''
                raise Exception(f'Invalid token in function declaration, expected "do" got "{code}"')
            if self.status == 'func.body':
                if self.func_build.add_token(code):
                    self.interpreter.layers[-1][self.func_build.name] = self.func_build
                    self.status = ''
                    self.interpreter.layer -= 1
                    return True
                return False
        if code == 'end':
            return True
        for layer in reversed(self.interpreter.layers):
            if code in layer:
                func: Function = layer[code]
                exec_func = func.start()
                if exec_func is not None:
                    self.interpreter.func_stack.append(exec_func)
                return False
        if code in ['func']:
            self.status = code
            return False
        if self.interpreter.parse_value(code):
            return False
        assert False, f'Invalid token "{code}"'

    def trace(self) -> str:
        return f'{self.scope.name}[{self.pointer}]'


class Function(Scope):
    ...


class Interpreter:
    def __init__(self):
        self.stack = []
        self.layers: list[dict] = []
        self.layer = 0

        self.builtins: dict[str, Builtin] = {
            'dump': Builtin('dump', 0, lambda: self.stack.append(f'[{", ".join(to_str(v, repr_=True) for v in self.stack)}]')),
            'here': Builtin('here', 0, lambda: self.stack.append(self.global_run.trace())),
            'stack': Builtin('stack', 0, lambda: self.stack.append(len(self.stack))),

            '~': Builtin('~', 1, lambda v: self.stack.append(~v)),
            '!': Builtin('!', 1, lambda v: self.stack.append(True if v == 0 else False)),
            'out': Builtin('out', 1, lambda v: print(to_str(v), end='')),
            'outln': Builtin('outln', 1, lambda v: print(v)),
            'in': Builtin('in', 1, lambda v: self.stack.append(input(v))),
            'inp': Builtin('inp', 1, lambda v: self.stack.append(parse_value(input(v)))),
            'dup': Builtin('dup', 1, lambda v: self.stack.extend((v, v))),
            'str': Builtin('str', 1, lambda v: self.stack.append(to_str(v))),
            'num': Builtin('num', 1, lambda v: self.stack.append(float(v))),
            'bool': Builtin('bool', 1, lambda v: self.stack.append(True if v == 'true' else False)),
            'type': Builtin('type', 1, lambda v: self.stack.append(True if v == 'true' else False)),
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
            'sth': Builtin('sth', 3, lambda c, b, a: self.stack.extend((c, a, b)))
        }

        self.global_scope = Scope('__global_scope__')
        self.global_run = self.global_scope.start()

    def add_token(self, code: str):
        self.global_scope.add_token(code, self)

    def execute(self):
        operation: Operation = self.global_run.get_next()
        operation.execute(self)

    def execute_all(self):
        while self.global_run.has_next():
            operation: Operation = self.global_run.get_next()
            operation.execute(self)

    def pop_stack(self, values):
        assert len(self.stack) >= values, f'Stack has not enough values (found {len(self.stack)}, expected {values})'
        return [self.stack.pop() for i in range(values)]