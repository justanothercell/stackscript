func splitStr do  // [str, token]
    0 store index  // [str, token]
    store token  // [str]
    store string  // []
    true while
        string index chrat  // [string.charAt(index)]
        token = dup if  // [bool]
            drop  // []
            string index split  // ["a", " b"]
            1 split swap drop  // ["a", "b"]
            token @splitStr @
            false true // ["a", "b", false, true]
        end
        ! if
            index 1 +  // [index+1]
            dup update index  // [index+1]
            string strlen <  // [bool]
            dup ! if
                string swap  // [str, bool]
            end
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