# -*- coding: utf-8 -*- #

module Rouge
  module Lexers
    class Stackscript < RegexLexer
      title     "stackscript"
      tag       'Stackscript'
      mimetypes 'text/x-stackscript'
      filenames '*.st'

      state:root do
          rule /(\/\/.*)/, Comment
          rule /(!\B|%\B|&\B|\*\B|\*\*\B|\+\B|-\B|\\/\B|<\B|<<\B|<=\B|=\B|>\B|>=\B|>>\B|@\B|\^\B|\|\B|~\B)/, String
          rule /(break\b|continue\b|delete\b|do\b|else\b|end\b|func\b |global\b|if\b|return\b|store\b|update\b|while\b)/, String
          rule /(clear\b|collect\b|drop\b|dump\b|dup\b|exit\b|expand\b|import\b|in\b|index\b|len\b|out\b|outln\b|pull\b|push\b|rem\b|sqrt\b|stacklen\b|sth\b|swap\b|trace\b)/, String
          rule /(true\b|false\b)/, Number
          rule /(\b\d+)/, Number
          rule /(std\b|math\b|builtins\b|os\b|types\b|io\b)/, Generic::Error
          rule /(\")/, String, :main__1
          rule /(\')/, String, :main__2
          rule /(\b[a-z][a-z0-9]*)/, Keyword
          rule /(\n|\r|\r\n)/, String
          rule /./, String
      end

      state:main__1 do
          rule /(\n|\r|\r\n)/, String
          rule /./, String
      end

      state:main__2 do
          rule /(\n|\r|\r\n)/, String
          rule /./, String
      end

    end
  end
end

