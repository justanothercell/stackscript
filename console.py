from interpreter import Interpreter


def run_console(stack_max=16, debug=False):
    interpreter = Interpreter()
    interpreter.run_repl(stack_max=stack_max, debug=debug)


if __name__ == '__main__':
    run_console(debug=False)