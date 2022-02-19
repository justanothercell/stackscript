func splitStr do  // [str, token]
    0 store index  // [str, token]
    store token  // [str]
    store string  // []
    true while
        string index chrat  // [string.charAt(index)]
        token = if
            string index split  // ["a", " b"]
            1 split swap drop  // ["a", "b"]
            token splitStr  // ["a", "b", "c"]
            string strlen update index  // ["a", "b", "c"]
        end
        index 1 +  // [index+1]
        dup update index  // [index+1]
        dup string strlen <  // [bool]
        swap string strlen = if  // [bool]
            string swap  // [str, bool]
        end
    end
end

"=== Split string by space ===" outln
true while
    clear
    "input: " in
    " " splitStr
    dump outln
    true
end