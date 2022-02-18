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
                self.interpreter.scope_stack.append(exec_func)
            return False
    if code in ['func']:
        self.status = code
        return False
    if self.interpreter.parse_value(code):
        return False
    assert False, f'Invalid token "{code}"'