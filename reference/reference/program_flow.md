#<a id="top"/>Program Flow
###### Go back to [README](../../README.md).
###### Go back to [reference](../reference.md).

---

There are different ways to control the program's flow.

`if's` test whether the topmost value of the stack is `true`. If yes, the if-scope is entered. 
Scopes are ended by using the keyword `end`.


<pre style="background-color:#272822;color:#dddddd;" spellcheck="false"><span style="color: rgb(170, 255, 255); background-color: rgb(39, 40, 34);" title="
STYLE : .constant
CONTEXT     : main::5
STACK : main::5 -> ANON::22
REGEX : (true\b|false\b)" onmouseover="this.style.backgroundColor='#3a3a3a'" onmouseout="this.style.backgroundColor='#272822'">true</span><span title="REGION NOT MATCHED

CONTEXT     : main::5
STACK : main::5 -> NOMATCH" onmouseover="this.style.backgroundColor='#442828'" onmouseout="this.style.backgroundColor='#272822'"> </span><span style="color:#a2f;" title="
STYLE : .special_token
CONTEXT     : main::5
STACK : main::5 -> ANON::14
REGEX : (break\b|continue\b|delete\b|do\b|else\b|end\b|func\b |global\b|if\b|return\b|store\b|update\b|while\b)" onmouseover="this.style.backgroundColor='#3a3a3a'" onmouseout="this.style.backgroundColor='#272822'">if</span>
<span title="REGION NOT MATCHED

CONTEXT     : main::5
STACK : main::5 -> NOMATCH" onmouseover="this.style.backgroundColor='#442828'" onmouseout="this.style.backgroundColor='#272822'" style="background-color: rgb(39, 40, 34);">    </span><span style="color: rgb(0, 119, 0); background-color: rgb(39, 40, 34);" title="
STYLE : .string
CONTEXT     : main::5
STACK : main::5 -> ANON::34
REGEX : (\&quot;)" onmouseover="this.style.backgroundColor='#3a3a3a'" onmouseout="this.style.backgroundColor='#272822'">"</span><span style="color: rgb(0, 119, 0); background-color: rgb(39, 40, 34);" title="
STYLE : .string
CONTEXT     : main::5
STACK : main::5 -> ANON::34 -> NOMATCH
REGEX : [NULL]" onmouseover="this.style.backgroundColor='#3a3a3a'" onmouseout="this.style.backgroundColor='#272822'">this will be executed</span><span style="color:#070;" title="
STYLE : .string
STACK : main::5 -> ANON::34 -> ANON::38
REGEX : (\&quot;)" onmouseover="this.style.backgroundColor='#3a3a3a'" onmouseout="this.style.backgroundColor='#272822'">"</span><span title="REGION NOT MATCHED

CONTEXT     : main::5
STACK : main::5 -> NOMATCH" onmouseover="this.style.backgroundColor='#442828'" onmouseout="this.style.backgroundColor='#272822'"> </span><span style="color: rgb(255, 136, 0); background-color: rgb(39, 40, 34);" title="
STYLE : .builtin
CONTEXT     : main::5
STACK : main::5 -> ANON::18
REGEX : (clear\b|collect\b|drop\b|dump\b|dup\b|exit\b|expand\b|import\b|in\b|index\b|len\b|out\b|outln\b|pull\b|push\b|rem\b|sqrt\b|stacklen\b|sth\b|swap\b|trace\b)" onmouseover="this.style.backgroundColor='#3a3a3a'" onmouseout="this.style.backgroundColor='#272822'">outln</span>
<span style="color: rgb(170, 34, 255); background-color: rgb(39, 40, 34);" title="
STYLE : .special_token
CONTEXT     : main::5
STACK : main::5 -> ANON::14
REGEX : (break\b|continue\b|delete\b|do\b|else\b|end\b|func\b |global\b|if\b|return\b|store\b|update\b|while\b)" onmouseover="this.style.backgroundColor='#3a3a3a'" onmouseout="this.style.backgroundColor='#272822'">end</span>
<span title="REGION NOT MATCHED

CONTEXT     : main::5
STACK : main::5 -> NOMATCH" onmouseover="this.style.backgroundColor='#442828'" onmouseout="this.style.backgroundColor='#272822'"></span>
<span style="color:#aff;" title="
STYLE : .number
CONTEXT     : main::5
STACK : main::5 -> ANON::26
REGEX : (\b\d+)" onmouseover="this.style.backgroundColor='#3a3a3a'" onmouseout="this.style.backgroundColor='#272822'">6</span><span title="REGION NOT MATCHED

CONTEXT     : main::5
STACK : main::5 -> NOMATCH" onmouseover="this.style.backgroundColor='#442828'" onmouseout="this.style.backgroundColor='#272822'"> </span><span style="color:#aff;" title="
STYLE : .number
CONTEXT     : main::5
STACK : main::5 -> ANON::26
REGEX : (\b\d+)" onmouseover="this.style.backgroundColor='#3a3a3a'" onmouseout="this.style.backgroundColor='#272822'">5</span><span title="REGION NOT MATCHED

CONTEXT     : main::5
STACK : main::5 -> NOMATCH" onmouseover="this.style.backgroundColor='#442828'" onmouseout="this.style.backgroundColor='#272822'" style="background-color: rgb(39, 40, 34);"> </span><span style="color:#ff0;" title="
STYLE : .op
CONTEXT     : main::5
STACK : main::5 -> ANON::10
REGEX : (!\B|%\B|&amp;\B|\*\B|\*\*\B|\+\B|-\B|\/\B|<\B|<<\B|<=\B|=\B|>\B|>=\B|>>\B|@\B|\^\B|\|\B|~\B)" onmouseover="this.style.backgroundColor='#3a3a3a'" onmouseout="this.style.backgroundColor='#272822'">*</span><span title="REGION NOT MATCHED

CONTEXT     : main::5
STACK : main::5 -> NOMATCH" onmouseover="this.style.backgroundColor='#442828'" onmouseout="this.style.backgroundColor='#272822'"> </span><span style="color: rgb(170, 255, 255); background-color: rgb(39, 40, 34);" title="
STYLE : .number
CONTEXT     : main::5
STACK : main::5 -> ANON::26
REGEX : (\b\d+)" onmouseover="this.style.backgroundColor='#3a3a3a'" onmouseout="this.style.backgroundColor='#272822'">32</span><span title="REGION NOT MATCHED

CONTEXT     : main::5
STACK : main::5 -> NOMATCH" onmouseover="this.style.backgroundColor='#442828'" onmouseout="this.style.backgroundColor='#272822'"> </span><span style="color: rgb(255, 255, 0); background-color: rgb(39, 40, 34);" title="
STYLE : .op
CONTEXT     : main::5
STACK : main::5 -> ANON::10
REGEX : (!\B|%\B|&amp;\B|\*\B|\*\*\B|\+\B|-\B|\/\B|<\B|<<\B|<=\B|=\B|>\B|>=\B|>>\B|@\B|\^\B|\|\B|~\B)" onmouseover="this.style.backgroundColor='#3a3a3a'" onmouseout="this.style.backgroundColor='#272822'">=</span><span title="REGION NOT MATCHED

CONTEXT     : main::5
STACK : main::5 -> NOMATCH" onmouseover="this.style.backgroundColor='#442828'" onmouseout="this.style.backgroundColor='#272822'" style="background-color: rgb(39, 40, 34);"> </span><span style="color: rgb(170, 34, 255); background-color: rgb(39, 40, 34);" title="
STYLE : .special_token
CONTEXT     : main::5
STACK : main::5 -> ANON::14
REGEX : (break\b|continue\b|delete\b|do\b|else\b|end\b|func\b |global\b|if\b|return\b|store\b|update\b|while\b)" onmouseover="this.style.backgroundColor='#3a3a3a'" onmouseout="this.style.backgroundColor='#272822'">if</span>
<span title="REGION NOT MATCHED

CONTEXT     : main::5
STACK : main::5 -> NOMATCH" onmouseover="this.style.backgroundColor='#442828'" onmouseout="this.style.backgroundColor='#272822'" style="background-color: rgb(39, 40, 34);">    </span><span style="color:#070;" title="
STYLE : .string
CONTEXT     : main::5
STACK : main::5 -> ANON::34
REGEX : (\&quot;)" onmouseover="this.style.backgroundColor='#3a3a3a'" onmouseout="this.style.backgroundColor='#272822'">"</span><span style="color: rgb(0, 119, 0); background-color: rgb(39, 40, 34);" title="
STYLE : .string
CONTEXT     : main::5
STACK : main::5 -> ANON::34 -> NOMATCH
REGEX : [NULL]" onmouseover="this.style.backgroundColor='#3a3a3a'" onmouseout="this.style.backgroundColor='#272822'">this will not be executed as 6 * 5 is not 32</span><span style="color:#070;" title="
STYLE : .string
STACK : main::5 -> ANON::34 -> ANON::38
REGEX : (\&quot;)" onmouseover="this.style.backgroundColor='#3a3a3a'" onmouseout="this.style.backgroundColor='#272822'">"</span><span title="REGION NOT MATCHED

CONTEXT     : main::5
STACK : main::5 -> NOMATCH" onmouseover="this.style.backgroundColor='#442828'" onmouseout="this.style.backgroundColor='#272822'"> </span><span style="color:#f80;" title="
STYLE : .builtin
CONTEXT     : main::5
STACK : main::5 -> ANON::18
REGEX : (clear\b|collect\b|drop\b|dump\b|dup\b|exit\b|expand\b|import\b|in\b|index\b|len\b|out\b|outln\b|pull\b|push\b|rem\b|sqrt\b|stacklen\b|sth\b|swap\b|trace\b)" onmouseover="this.style.backgroundColor='#3a3a3a'" onmouseout="this.style.backgroundColor='#272822'">outln</span>
<span style="color: rgb(170, 34, 255); background-color: rgb(39, 40, 34);" title="
STYLE : .special_token
CONTEXT     : main::5
STACK : main::5 -> ANON::14
REGEX : (break\b|continue\b|delete\b|do\b|else\b|end\b|func\b |global\b|if\b|return\b|store\b|update\b|while\b)" onmouseover="this.style.backgroundColor='#3a3a3a'" onmouseout="this.style.backgroundColor='#272822'">end</span></pre>