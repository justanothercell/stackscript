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
Update a :
```
1 store x
```

To get the value of a variable, simply write its name


---
### Function and Variable Pointers
###### Go to [top](#variables--modules).

---

### Modules
###### Go to [top](#variables--modules).