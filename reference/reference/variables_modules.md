# Variables & Modules
###### Go back to [README](../../README.md).
###### Go back to [reference](../reference.md).
###### [Previous](structure_syntax_builtins.md)

---

###### Go down to [Variables](#Variables).
###### Go down to [Function and Variable Pointers](#Function-and-Variable-Pointers).
###### Go down to [Modules](#Modules).

---

### Variables
###### Go to [top](#variables--modules).
As you write more complex programs, you will notice it can be quite cumbersome and confusing to access variables buried
deep inside the stack, or variables that you need a lot. 

For this reason variables exist. Same as functions, variables are accessible in the scope they are created in
and any "child" scopes.

Functions can be [named](program_flow.md#functions) the same way as variables. 

Create a variable named `x` with the value `1` in local scope:
```
1 store x
```
Create a variable named `mytext` with the value `"wasd"` in global scope:<br>
(Use this feature sparingly. In most cases just initialize the variable with a dummy value at the beginning and later update
it from within a scope)
```
"wasd" global mytext
```
Delete the variable named `x`:
```
delete x
```
Update `mytext` from an inner scope instead of creating a new one with the same name:
```
"not wasd any more" update mytext
```

To get the value of a variable, simply write its name:
```
// in console:
# mytext
["not wasd any more"]
#
```

---
### Function and Variable Pointers
###### Go to [top](#variables--modules).
To reference a variable and not just its value, or give a function as an argument to another function, you can store a
reference to it on the stack. To do this, put an `@` directly in front of it:
```
// in console:
# 1 2 @+
[1, 2, @+]
#
```
To call the stored variable/function, write again a single `@`, this time as a separate command.
This will execute the referenced `+` and add the `1` and `2`.
```
// in console:
# @
[3]
#
```
A (more or less useful) example:
```
// in console:
# func log_exec do
#.. dup "operation is: " out outln
#.. @ "result is: " out outln
#.. end
[]
# 3 5
[3, 5]
# @**
[3, 5, @**]
# log_exec
operation is: @**
result is: 243
[]
#
```

---

### Modules
###### Go to [top](#variables--modules).
You can import a module from the [lib](../../lib) folder.
Paths are provided with `.` instead of `/`. Dots in names are not supported.
Stackscript will search whether a `.st` and `.st.py` file with the specified path exists. 
```
// in console:
# "std.math" import
[std.math]
#
```
This will append a reference to an "instance" of the standard math to the stack.
That way, modules can also be used as classes/objects, as each "instance" keeps track of
its own variables. BUT: it does **not** have its own stack.
Although it's usable that way, usually modules are imported and directly stored into variables:
```
// in console:
# "std.math" import store math
[]
#
```
To access a module function or variable (which are not updatable from the outside), put the module onto the stack and write a `:` directly in front
of the name you want to access:
(Note the space in front of the colon)
```
// in console:
# math :pi
[3.141592653589793]
# math :sin
[1.2246467991473532e-16]
```
These attributes are of course also able to be referenced:
```
// in console:
# clear
[]
# math @:sin
[std.math @:sin]
# 2 swap
[2, std.math @:sin]
# @
[0.9092974268256817]
#
```

Variables from modules can be put into global scope, by using the `global` attribute when creating them.
This should be used sparingly and only when the user is fully aware of the consequences (such as inmporting all standard
modules with the [std](../../lib/std.st) module for convenience: `"std" import drop`) as it can overwrite variables the programmer
might already have named that way.

[std.builtins](../../lib/std/builtins.st.py) is usable by default without having to prefix `builtins`, although of course it can be imported using
`"std.builtins" import store builtins` and used like any other module.

If you want to create modules yourself, take a look at [std.math](../../lib/std/math.st.py) for how to map a python module
to a stackscript module (has to end in `.st.py` to be recognized) and [std.io](../../lib/std/io.st) on how to write a
native stackscript one, which uses its [std.fileio.file](../../lib/std/fileio/file.st) as a "class" for file access.

---

###### Go to [top](#variables--modules).
Congratulations, you have reached the end!<br>
Feel free to browse the
[examples](../../examples/examples.md), code for yourself or report [issues or feature requests](https://github.com/DragonFIghter603/stackscript/issues). 
