#<a id="top"/>Program Flow
###### Go back to [README](../../README.md).
###### Go back to [reference](../reference.md).

---

### If - Else

An `if` tests whether the topmost value of the stack is `true`. If yes, the if-scope is entered. 
Scopes are ended by using the keyword `end`. Optionally, you can add an `else`...`end` block 
directly after the `if`...`end`. Any operations between the if and else will not work.

<img align="left" src="if-else.png">

<br>

```
true if
    "this will be executed" outln
end


4 6 * 32 = if
    "this won't be executed" outln
    "as 4 * 6 is not 32" outln
end
else
    "this will be executed, because" outln
    the condition returned false" outln
end
```
