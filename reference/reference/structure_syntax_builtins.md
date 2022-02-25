#<a id="top"/>Structure, Syntax & Builtins
###### Go back to [README](../../README.md).
###### Go back to [reference](../reference.md).
###### Go to [builtins](#builtins).
### Structure & Syntax
Stackscript is made of two main components: the stack and the... variable stack.
Let's first focus on the normal stack. (You can learn more about variables [here](variables_modules.md))

You can follow the explanation with the command line interface by executing [console.py](../../console.py).

---
###### Go to [top](#top).
To add a value to the stack, simply write it and pressing enter:
`1`<kbd>Enter</kbd><br>
Valid values are: `ints/floats`, `true/false` and `"strings"`.

The stack shows up as a list by default after every line as a list, the right side representing the top: <br>
`["path/to/console.py", 1]`
<br>
The command line arguments (here only the paht of the executed file) are on the stack by default.
If you want to clear the stack, simply write `clear`.<br>
`[]`<br>
Tokens are separated by either whitespace or a newline. That means you can write multiple instructions into one line:
`42 96`. This will push both values onto the stack.<br>
`[42, 96]`

---
###### Go to [top](#top).
Now let's add the two values on the stack. To execute an operation, simply write it: `+`.
The operation will take as many values as it needs from the stack, in this case two (a + b).
After the execution of the operation, the result will be appended onto the stack again.<br>
`[138]`<br>
If an operation doesn't find enough values, it will throw an error.

Onto something more difficult:<br>
We want to find out what the previously computed `138` times `(8-6)` is. To do that, we first add `8`and `6` onto the stack,
then execute minus, popping `8` and `6` off the stack and returning `2` onto the stack, and then execute multiplication:
`8 6 - *` (note that a whitespace is required after each token and that the `138` is still on the stack. If you cleared she stack before, the `*` will onyl find one value and throw an error).<br>
`[276]`<br>
As we can see the result is `276`! Good job!

---
###### Go to [top](#top).
As you might have seen, the operations pop their arguments off the stack.
This is less than ideal when it is important to keep the original value for later use.
We now want to get the quarter of the result of last time, but keep that original value:
`dup 4 /`. `dup` duplicates the last value onto the stack. We then can add `4` to the stack and divide the duplicated value by it.<br>
`[276, 69]`<br>
As you can see, the result is `69` and the original value is still on the stack!

One last function before letting you try soemthing out in your own: `swap`<br>
As the name implies, `swap` swaps the last two values of the stack. This is importnt for example for the 
order of division or subraction.<br>
`swap`<br>
`[69, 276]`<br>
`/`<br>
`[0.25]`<br>

---
###### Go to [top](#top).
Take a look at the builtins and try out some calculations to wrap your head around this unusual concept.
Once you have tried out a bit, go [here](variables_modules.md) for more advanced concepts.

###<a id="builtins"/>Builtins
These operators work exactly like in python, for example: `a b + -> a + b`

`% & * ** + - / < << <= = > >= >> ^ | ~`

Special operators:<br>
`!` not operator, inverts `true`/`false`<br>
`@` function reference

| function  | description |
| --------- | --------- |
| clear     | clears stack |
| collect   | a, b, c, ..., len -> [a, b, c, ...] |
| expand    | [a, b, c, ...] -> a, b, c, ..., len |
| drop      | drops last value off stack |
| dump      | appends a string representation of itself to the stack |
| dup       | a -> a, a |
| exit      | a -> exit(a) |
| import    | imports [module](variables_modules.md) |
| in        | a -> input(a) |
| index     | a, i -> a[i] (works for array/str) |
| len       | a -> len(a) |
| out       | a -> print(a, end='') |
| outln     | a -> print(a) |
| pull      | n -> pulls the nth element onto the top of the stack |
| push      | a, n -> pushes a n places into the stack |
| rem       | n -> drops the last n elements |
| sqrt      | a -> sqrt(a) |
| stacklen  | length of stack |
| sth       | a, b, c -> c, a, b |
| swap      | a, b -> b, a |
| trace     | adds a function trace string onto the stack |