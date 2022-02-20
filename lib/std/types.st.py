from interpreter import Builtin, get_type, parse_value, to_str


def export():
    #  sqrt and pow are already in the builtins, will be left here though for completeness
    values = {
        'parse': Builtin('parse', 1, lambda interpreter, v: interpreter.stack.append(parse_value(v))),
        'num': Builtin('num', 1, lambda interpreter, v: interpreter.stack.append(float(v))),
        'bool': Builtin('bool', 1, lambda interpreter, v: interpreter.stack.append(True if v == 'true' else False)),
        'type': Builtin('type', 1, lambda interpreter, v: get_type(v)),
        'str': Builtin('str', 1, lambda interpreter, v: interpreter.stack.append(to_str(v))),
        'strlen': Builtin('strlen', 1, lambda interpreter, v: interpreter.stack.append(len(v))),
        'chr': Builtin('str', 1, lambda interpreter, v: interpreter.stack.append(ord(v))),
        'ord': Builtin('str', 1, lambda interpreter, v: interpreter.stack.append(chr(v))),

        'chrat': Builtin('chrat', 2, lambda interpreter, b, a: interpreter.stack.append(a[b])),  # str(a) index(b)
        'splitat': Builtin('splitat', 2, lambda interpreter, b, a: interpreter.stack.extend((a[:b], a[b:]))),
    }
    return values
