import sys

import math

from interpreter import Builtin, Variable, Interpreter


def export():
    #  sqrt and pow are already in the builtins, will be left here though for completeness
    values = {
        'acos': Builtin('acos', 1, lambda interpreter, v: interpreter.stack.append(math.acos(v))),
        'acosh': Builtin('acosh', 1, lambda interpreter, v: interpreter.stack.append(math.acosh(v))),
        'asin': Builtin('asin', 1, lambda interpreter, v: interpreter.stack.append(math.asin(v))),
        'asinh': Builtin('asinh', 1, lambda interpreter, v: interpreter.stack.append(math.asinh(v))),
        'atan': Builtin('atan', 1, lambda interpreter, v: interpreter.stack.append(math.atan(v))),
        'atanh': Builtin('atanh', 1, lambda interpreter, v: interpreter.stack.append(math.atanh(v))),
        'ceil': Builtin('ceil', 1, lambda interpreter, v: interpreter.stack.append(math.ceil(v))),
        'cos': Builtin('cos', 1, lambda interpreter, v: interpreter.stack.append(math.cos(v))),
        'cosh': Builtin('cosh', 1, lambda interpreter, v: interpreter.stack.append(math.cosh(v))),
        'degrees': Builtin('degrees', 1, lambda interpreter, v: interpreter.stack.append(math.degrees(v))),
        'erf': Builtin('erf', 1, lambda interpreter, v: interpreter.stack.append(math.erf(v))),
        'erfc': Builtin('erfc', 1, lambda interpreter, v: interpreter.stack.append(math.erfc(v))),
        'exp': Builtin('exp', 1, lambda interpreter, v: interpreter.stack.append(math.exp(v))),
        'expm1': Builtin('expm1', 1, lambda interpreter, v: interpreter.stack.append(math.expm1(v))),
        'fabs': Builtin('fabs', 1, lambda interpreter, v: interpreter.stack.append(math.fabs(v))),
        'factorial': Builtin('factorial', 1, lambda interpreter, v: interpreter.stack.append(math.factorial(v))),
        'floor': Builtin('floor', 1, lambda interpreter, v: interpreter.stack.append(math.floor(v))),
        'frexp': Builtin('frexp', 1, lambda interpreter, v: interpreter.stack.append(math.frexp(v))),
        'fsum': Builtin('fsum', 1, lambda interpreter, v: interpreter.stack.append(math.fsum(v))),
        'gamma': Builtin('gamma', 1, lambda interpreter, v: interpreter.stack.append(math.gamma(v))),
        'gcd': Builtin('gcd', 1, lambda interpreter, v: interpreter.stack.append(math.gcd(v))),
        'hypot': Builtin('hypot', 1, lambda interpreter, v: interpreter.stack.append(math.hypot(v))),
        'isfinite': Builtin('isfinite', 1, lambda interpreter, v: interpreter.stack.append(math.isfinite(v))),
        'isinf': Builtin('isinf', 1, lambda interpreter, v: interpreter.stack.append(math.isinf(v))),
        'isnan': Builtin('isnan', 1, lambda interpreter, v: interpreter.stack.append(math.isnan(v))),
        'isqrt': Builtin('isqrt', 1, lambda interpreter, v: interpreter.stack.append(math.isqrt(v))),
        'lcm': Builtin('lcm', 1, lambda interpreter, v: interpreter.stack.append(math.lcm(v))),
        'lgamma': Builtin('lgamma', 1, lambda interpreter, v: interpreter.stack.append(math.lgamma(v))),
        'log': Builtin('log', 1, lambda interpreter, v: interpreter.stack.append(math.log(v))),
        'log1p': Builtin('log1p', 1, lambda interpreter, v: interpreter.stack.append(math.log1p(v))),
        'log10': Builtin('log10', 1, lambda interpreter, v: interpreter.stack.append(math.log10(v))),
        'log2': Builtin('log2', 1, lambda interpreter, v: interpreter.stack.append(math.log2(v))),
        'modf': Builtin('modf', 1, lambda interpreter, v: interpreter.stack.append(math.modf(v))),
        'radians': Builtin('radians', 1, lambda interpreter, v: interpreter.stack.append(math.radians(v))),
        'sin': Builtin('sin', 1, lambda interpreter, v: interpreter.stack.append(math.sin(v))),
        'sinh': Builtin('sinh', 1, lambda interpreter, v: interpreter.stack.append(math.sinh(v))),
        'sqrt': Builtin('sqrt', 1, lambda interpreter, v: interpreter.stack.append(math.sqrt(v))),
        'tan': Builtin('tan', 1, lambda interpreter, v: interpreter.stack.append(math.tan(v))),
        'tanh': Builtin('tanh', 1, lambda interpreter, v: interpreter.stack.append(math.tanh(v))),
        'trunc': Builtin('trunc', 1, lambda interpreter, v: interpreter.stack.append(math.trunc(v))),
        'prod': Builtin('prod', 1, lambda interpreter, v: interpreter.stack.append(math.prod(v))),
        'perm': Builtin('perm', 1, lambda interpreter, v: interpreter.stack.append(math.perm(v))),
        'ulp': Builtin('ulp', 1, lambda interpreter, v: interpreter.stack.append(math.ulp(v))),

        'atan2': Builtin('atan2', 1, lambda interpreter, a, b: interpreter.stack.append(math.atan2(a, b))),
        'comb': Builtin('comb', 1, lambda interpreter, a, b: interpreter.stack.append(math.comb(a, b))),
        'copysign': Builtin('copysign', 1, lambda interpreter, a, b: interpreter.stack.append(math.copysign(a, b))),
        'dist': Builtin('dist', 1, lambda interpreter, a, b: interpreter.stack.append(math.dist(a, b))),
        'fmod': Builtin('fmod', 1, lambda interpreter, a, b: interpreter.stack.append(math.fmod(a, b))),
        'ldexp': Builtin('ldexp', 1, lambda interpreter, a, b: interpreter.stack.append(math.ldexp(a, b))),
        'nextafter': Builtin('nextafter', 1, lambda interpreter, a, b: interpreter.stack.append(math.nextafter(a, b))),
        'pow': Builtin('pow', 1, lambda interpreter, a, b: interpreter.stack.append(math.pow(a, b))),
        'remainder': Builtin('remainder', 1, lambda interpreter, a, b: interpreter.stack.append(math.remainder(a, b))),
        'isclose': Builtin('isclose', 1, lambda interpreter, a, b: interpreter.stack.append(math.isclose(a, b))),

        'pi': Variable('tau', math.pi),
        'e': Variable('tau', math.e),
        'tau': Variable('tau', math.tau)
    }
    return values
