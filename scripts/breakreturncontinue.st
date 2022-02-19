func test do
    1 2 3
    return
    4 5 6
end
test
dump outln
clear

func test2 do
    store x
    1 2 3
    x if "4a" return 5 end
    else "4b" return 5 end
    6 7 8
end
false test2
true test2
dump outln
clear

10 true while
    dup out
    1 - dup 0 >
    swap dup 5 > if
        swap continue
    end
    swap
    " after " out
end
"" outln
dump outln
clear

10 true while
    dup out " " out
    dup 5 < if
        break
    end
    1 - dup 0 >
end
"" outln
dump outln
clear