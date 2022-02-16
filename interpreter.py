import ast


class Executable:
    def __init__(self, args: int, func):
        self.args = args
        self.func = func


class Function:
    def __init__(self, args: int, func):
        self.args = args
        self.func = func


class Interpreter:
    def __init__(self, debug=False):
        self.stack = []
        self.layers = [{}]
        self.status = ''
        self.debug = debug

    def add_token(self, code: str):
        if code == '':
            return
        if code == 'dump':
            print(self.stack)
            return
        if self.status != '':
            if self.status == 'func':
                if code.isidentifier() and code not in ['out', 'outln', 'in', 'inp', 'dup', 'drop', 'swap', 'dump', 'while', 'func', 'if']:
                    self.status = 'func.named'
                    return
                self.status = ''
                raise Exception(f'Invalid name "{code}" for function')
            if self.status == 'func.named':
                if code == 'do':
                    self.status = ''
                    self.layers.append({})
                    return
                self.status = ''
                raise Exception(f'Invalid token in function declaration, expected "do" got "{code}"')

        if code in ['while', 'func', 'if']:
            self.status = code
            return
        if self.parse_value(code):
            return
        if code in ['~', 'out', 'outln', 'in', 'inp', 'dup', 'drop']:
            v, = self.pop_stack(1)
            try:
                if code == '~':
                    self.stack.append(~v)
                elif code == 'out':
                    print(v, end='')
                elif code == 'outln':
                    print(v)
                    pass
                elif code == 'in':
                    self.stack.append(input(v))
                elif code == 'inp':
                    self.parse_value(input(v))
                elif code == 'dup':
                    self.stack.append(v)
                    self.stack.append(v)
                elif code == 'drop':
                    pass
            except TypeError:
                raise Exception(f'Invalid operation "{code}" for {v}')
            return
        if code in ['+', '-', '*', '/', '**', '%', '|', '^', '&', '>>', '<<', '=', '>', '<', '>=', '<=', 'swap']:
            b, a = self.pop_stack(2)  # x, y, z, a, b is going to be popped first b then a
            try:
                if code == '+':
                    self.stack.append(a + b)
                elif code == '-':
                    self.stack.append(a - b)
                elif code == '*':
                    self.stack.append(a * b)
                elif code == '/':
                    self.stack.append(a / b)
                elif code == '**':
                    self.stack.append(a ** b)
                elif code == '%':
                    self.stack.append(a % b)
                elif code == '|':
                    self.stack.append(a | b)
                elif code == '^':
                    self.stack.append(a ^ b)
                elif code == '&':
                    self.stack.append(a & b)
                elif code == '>>':
                    self.stack.append(a >> b)
                elif code == '<<':
                    self.stack.append(a << b)
                elif code == '=':
                    self.stack.append(a == b)
                elif code == '>':
                    self.stack.append(a > b)
                elif code == '<':
                    self.stack.append(a < b)
                elif code == '>=':
                    self.stack.append(a >= b)
                elif code == '<=':
                    self.stack.append(a <= b)
                elif code == 'swap':
                    self.stack.append(b)
                    self.stack.append(a)
            except TypeError:
                raise Exception(f'Invalid operation "{code}" for {b, a}')
            return
        if code in ['sth']:
            c, b, a = self.pop_stack(3)
            try:
                if code == 'sth':  # a b c -> c a b
                    self.stack.append(c)
                    self.stack.append(a)
                    self.stack.append(b)
            except TypeError:
                raise Exception(f'Invalid operation "{code}" for {c, b, a}')
            return
        if code == 'end':
            assert len(self.layers) > 1, 'Program is not in scoped context!'
            self.layers.pop()
            return
        assert False, f'Invalid token "{code}"'

    def pop_stack(self, values):
        assert len(self.stack) >= values, f'Stack has not enough values (found {len(self.stack)}, expected {values})'
        return [self.stack.pop() for i in range(values)]

    def parse_value(self, code):
        if code in ['true', 'false']:
            self.stack.append(True if code == 'true' else False)
            return True
        if (code.startswith('"') and code.endswith('"')) or (code.startswith('\'') and code.endswith('\'')):
            self.stack.append(ast.literal_eval(code))
            return True
        if code.isnumeric():
            self.stack.append(int(code))
            return True
        return False


