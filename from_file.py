from interpreter import Interpreter


def run_file(file: str, debug=False):
    interpreter = Interpreter()
    with open(file, 'r') as script:
        interpreter.parse(script.read())
    interpreter.execute_all(debug=debug)


if __name__ == '__main__':
    run_file('scripts/power.st', debug=False)
