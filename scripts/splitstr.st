"std.types" import store types

func splitStr do
    0 store index
    store token
    store string
    true while
        string types :strlen 0 = if
            break
        end
        string index types :chrat
        token = if
            string index types :splitat
            1 types :splitat swap drop
            token splitStr
            string types :strlen update index
        end
        index 1 +
        dup dup update index
        string types :strlen >= if
            string types :strlen = if
                string break
            end
            break
        end
        drop
        true
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