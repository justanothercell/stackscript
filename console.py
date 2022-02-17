import sys
import shlex

from interpreter import Interpreter, InvalidToken


def run_console():
    interpreter = Interpreter()
    while True:
        try:
            print('# ' if interpreter.layer == 0 else '. ' * interpreter.layer, end='')
            inp = input()
            try:
                tokens = shlex.split(inp, posix=False)
            except ValueError as e:
                sys.stderr.write(str(e) + '\n')
                sys.stderr.flush()
                print('', end='')
                continue
            for token in tokens:
                interpreter.add_token(token)
                interpreter.execute_all()
        except InvalidToken as i:
            sys.stderr.write(f'Invalid token "{str(i)}"\n')
            sys.stderr.flush()
            print('', end='')
        except AssertionError as e:
            sys.stderr.write(str(e) + '\n')
            sys.stderr.flush()
            print('', end='')


if __name__ == '__main__':
    run_console()
