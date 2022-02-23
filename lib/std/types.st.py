from interpreter import Builtin, get_type, parse_value, to_str, lenlist


def bytes_to_ints(b):
    assert isinstance(b, bytes), '"ints" expects bytes'
    return list(b)


def export():
    #  sqrt and pow are already in the builtins, will be left here though for completeness
    values = {
        'parse': Builtin('parse', 1, lambda interpreter, v: interpreter.stack.append(parse_value(v))),
        'num': Builtin('num', 1, lambda interpreter, v: interpreter.stack.append(float(v))),
        'bool': Builtin('bool', 1, lambda interpreter, v: interpreter.stack.append(True if v == 'true' else False)),
        'type': Builtin('type', 1, lambda interpreter, v: get_type(v)),
        'str': Builtin('str', 1, lambda interpreter, v: interpreter.stack.append(to_str(v))),
        'bytes': Builtin('bytes', 1, lambda interpreter, v: interpreter.stack.append(bytes(v))),
        'bints': Builtin('bints', 1, lambda interpreter, v: interpreter.stack.append(bytes_to_ints(v))),
        'chr': Builtin('str', 1, lambda interpreter, v: interpreter.stack.append(ord(v))),
        'ord': Builtin('str', 1, lambda interpreter, v: interpreter.stack.append(chr(v))),
        'encode': Builtin('encode', 2, lambda interpreter, a, b: interpreter.stack.append(a.encode(b))),

        'splitat': Builtin('splitat', 2, lambda interpreter, a, b: interpreter.stack.extend((a[:b], a[b:]))),
        'split': Builtin('splittoken', 2, lambda interpreter, a, b: interpreter.stack.append(a.split(b))),
        # to_str(v) for v in interpreter.pop_stack(a)
        'join': Builtin('join', 2, lambda interpreter, a, b: interpreter.stack.append(b.join(a))),

        'decode': Builtin('decode', 2, lambda interpreter, a, b: interpreter.stack.append(bytes(a).decode(b))),
    }
    return values
# 'std.types' import store types
# "mystr" 'utf-8' types :encode
# 'utf-8' types :decode
# "std.types" import store types "/" types :split "." types :join

