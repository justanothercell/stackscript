from pygments.lexer import RegexLexer, bygroups
from pygments.token import *

import re

__all__=['StackscriptLexer']

class StackscriptLexer(RegexLexer):
    name = 'Stackscript'
    aliases = ['stackscript']
    filenames = ['*.st']
    flags = re.MULTILINE | re.UNICODE

    tokens = {
        'root' : [
            (u'(//.*)', bygroups(Comment)),
            (u'(!\\B|%\\B|&\\B|\\*\\B|\\*\\*\\B|\\+\\B|-\\B|\\/\\B|<\\B|<<\\B|<=\\B|=\\B|>\\B|>=\\B|>>\\B|@\\B|\\^\\B|\\|\\B|~\\B)', bygroups(String)),
            (u'(break\\b|continue\\b|delete\\b|do\\b|else\\b|end\\b|func\\b |global\\b|if\\b|return\\b|store\\b|update\\b|while\\b)', bygroups(String)),
            (u'(clear\\b|collect\\b|drop\\b|dump\\b|dup\\b|exit\\b|expand\\b|import\\b|in\\b|index\\b|len\\b|out\\b|outln\\b|pull\\b|push\\b|rem\\b|sqrt\\b|stacklen\\b|sth\\b|swap\\b|trace\\b)', bygroups(String)),
            (u'(true\\b|false\\b)', bygroups(Number)),
            (u'(\\b\\d+)', bygroups(Number)),
            (u'(std\\b|math\\b|builtins\\b|os\\b|types\\b|io\\b)', bygroups(Generic.Error)),
            (u'(\\\")', bygroups(String), 'main__1'),
            (u'(\\\')', bygroups(String), 'main__2'),
            (u'(\\b[a-z][a-z0-9]*)', bygroups(Keyword)),
            ('(\n|\r|\r\n)', String),
            ('.', String),
        ],
        'main__1' : [
            ('(\n|\r|\r\n)', String),
            ('.', String),
        ],
        'main__2' : [
            ('(\n|\r|\r\n)', String),
            ('.', String),
        ]
    }

