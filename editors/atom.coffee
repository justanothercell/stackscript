'fileTypes' : [
  'st'
]
'name' : 'stackscript'
'patterns' : [
  {
    'include' : '#main'
  }
]
'scopeName' : 'source.stackscript'
'uuid' : ''
'repository' : {
  'main' : {
    'patterns' : [
      {
        'match' : '(//.*)'
        'name' : 'comment.stackscript'
      }
      {
        'match' : '(!\\B|%\\B|&\\B|\\*\\B|\\*\\*\\B|\\+\\B|-\\B|\\/\\B|<\\B|<<\\B|<=\\B|=\\B|>\\B|>=\\B|>>\\B|@\\B|\\^\\B|\\|\\B|~\\B)'
        'name' : 'text.stackscript'
      }
      {
        'match' : '(break\\b|continue\\b|delete\\b|do\\b|else\\b|end\\b|func\\b |global\\b|if\\b|return\\b|store\\b|update\\b|while\\b)'
        'name' : 'text.stackscript'
      }
      {
        'match' : '(clear\\b|collect\\b|drop\\b|dump\\b|dup\\b|exit\\b|expand\\b|import\\b|in\\b|index\\b|len\\b|out\\b|outln\\b|pull\\b|push\\b|rem\\b|sqrt\\b|stacklen\\b|sth\\b|swap\\b|trace\\b)'
        'name' : 'text.stackscript'
      }
      {
        'match' : '(true\\b|false\\b)'
        'name' : 'constant.numeric.stackscript'
      }
      {
        'match' : '(\\b\\d+)'
        'name' : 'constant.numeric.stackscript'
      }
      {
        'match' : '(std\\b|math\\b|builtins\\b|os\\b|types\\b|io\\b)'
        'name' : 'invalid.stackscript'
      }
      {
        'begin' : '(\\")'
        'beginCaptures' : {
          '1' : {
            'name' : 'text.stackscript'
          }
        }
        'contentName' : 'text.stackscript'
        'end' : '(\\")'
        'endCaptures' : {
          '1' : {
            'name' : 'text.stackscript'
          }
        }
      }
      {
        'begin' : '(\\\')'
        'beginCaptures' : {
          '1' : {
            'name' : 'text.stackscript'
          }
        }
        'contentName' : 'text.stackscript'
        'end' : '(\\\')'
        'endCaptures' : {
          '1' : {
            'name' : 'text.stackscript'
          }
        }
      }
      {
        'match' : '(\\b[a-z][a-z0-9]*)'
        'name' : 'keyword.stackscript'
      }
    ]
  }
  'main__1' : {
    'patterns' : [
    ]
  }
  'main__2' : {
    'patterns' : [
    ]
  }
}
