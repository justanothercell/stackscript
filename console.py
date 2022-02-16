import sys
import shlex

from interpreter import Interpreter


def run_console(debug=False):
    interpreter = Interpreter(debug=debug)
    while True:
        try:
            print('# ' if len(interpreter.layers) < 1 else '. ' * len(interpreter.layers), end='')
            inp = input()
            tokens = shlex.split(inp, posix=False)
            for token in tokens:
                interpreter.add_token(token)
        except Exception as e:
            sys.stderr.write(str(e)+'\n')
            sys.stderr.flush()
            print('', end='')


if __name__ == '__main__':
    run_console(True)
