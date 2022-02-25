"std.types" import store types

func splitStr do
    0 store i
    store token
    store string
    true while
        string len 0 = if
            break
        end
        string i index token = if
            string i types :splitat
            1 types :splitat swap drop
            token splitStr
            string len update i
        end
        i 1 +
        dup dup update i
        string len >= if
            string len = if
                string
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