"std" import drop

// rule 30
// https://mathworld.wolfram.com/CellularAutomaton.html

func getrule do  // a, b, c -> follow_rule
   // calc binary pattern 0bABC
   sth   // c, a, b
   swap 2 <<  // c, b, a00
   sth   // a00, c, b
   1 <<  // a00, c, b0
   + +   // 0bABC
   dup 0 = if drop 0 return end
   dup 1 = if drop 1 return end
   dup 2 = if drop 1 return end
   dup 3 = if drop 1 return end
   dup 4 = if drop 1 return end
   dup 5 = if drop 0 return end
   dup 6 = if drop 0 return end
   dup 7 = if drop 0 return end
end

func evolve do
    0 swap expand 0 swap 2 + collect store list
    list len store l
    1 store i
    i 1 + l < while
        list i 1 - index  // a
        list i index      // b
        list i 1 + index  // c
        getrule
        i 1 + update i
        i 1 + l <
    end
    l 2 - collect 0 swap expand 0 swap 2 + collect
end

func plotline do  // arr, maxwidth
    store w
    expand store l
    w 2 * 3 + l - 2 / store s
    0 store i
    i s < while
        " " out
        i 1 + update i
        i s <
    end
    0 store i
    i l < while
        1 = if "X" out end
        else " " out end
        i 1 + update i
        i l <
    end
    "" outln
end

func rule30pyramid do  // linescount
    0 store i
    store lines
    0 1 0 3 collect dup lines plotline  // start: [0, 1, 0]
    i lines < while
        evolve dup lines plotline
        i 1 + update i
        i lines <
    end
end

func rule30lines do  // linescount
    0 store i
    store lines
    "cls" os :system drop
    0 1 0 3 collect dup lines plotline  // start: [0, 1, 0]
    i lines < while
        "" in drop
        "cls" os :system drop
        evolve dup lines plotline
        i 1 + update i
        i lines <
    end
end

// uncomment to draw the classic "pyramid"
16 rule30pyramid

// uncomment to clear after every line and show each state "seperately". press enter for next line
// pycharm doesnt work with this, but any regular command line works
// 32 rule30lines