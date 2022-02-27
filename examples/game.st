"std" import drop

func getaction do
    inch types :bints expand drop
    dup 3 = if 0 exit end  // exit on Crtl+C
    224 = if  // pre-code for special keys
        inch types :bints expand drop  // actual code
        dup 72 = if drop 0 return end  // up
        dup 80 = if drop 1 return end  // down
        dup 75 = if drop 2 return end  // left
        dup 77 = if drop 3 return end  // right
    end
    -1
end

func start do
    clear

    // https://patorjk.com/software/taag
    "     _       _                 _              _           \n"
    "    / \\   __| |_   _____ _ __ | |_ _   _ _ __(_) ___ __ _ \n" +
    "   / _ \\ / _` \\ \\ / / _ \\ '_ \\| __| | | | '__| |/ __/ _` |\n" +
    "  / ___ \\ (_| |\\ V /  __/ | | | |_| |_| | |  | | (_| (_| |\n" +
    " /_/   \\_\\__,_| \\_/ \\___|_| |_|\\__|\\__,_|_|  |_|\\___\\__,_|\n" +
    "     A game made in stackscript for testing purposes,\n" +
    "           and sounds way cooler than it is." +
    store title

    51 global xsize
    21 global ysize

    4 global xpos
    4 global ypos

    10 global maxhp
    maxhp global hp
    0 global coins

    1 1 1 1 1 1 1 1 1 1   1 1 1 1 1 1 1 1 1 1   1 1 1 1 1 1 1 1 1 1   1 1 1 1 1 1 1 1 1 1   1 1 1 1 1 1 0 0 0 1  1 xsize collect
    1 0 0 0 0 0 0 0 0 0   0 0 1 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0 0 0   0 0 0 1 0 0 0 0 0 0   0 0 0 0 0 0 0 0 0 0  1 xsize collect
    1 0 0 0 0 0 0 0 0 0   0 0 1 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0 0 0   0 0 0 1 0 0 0 0 0 0   3 0 0 0 0 0 0 0 0 0  1 xsize collect
    1 0 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0 3 0   0 0 0 0 0 2 0 0 0 0   0 0 0 1 0 0 2 0 2 3   0 3 0 0 0 3 0 0 0 0  1 xsize collect
    1 0 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0 0 0   0 0 0 1 2 2 2 3 3 2   2 0 3 3 3 0 0 0 0 0  1 xsize collect
    1 0 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0 0 0   0 0 0 1 2 3 2 3 2 2   2 3 0 0 0 2 2 2 0 0  1 xsize collect
    1 0 0 0 0 0 0 0 0 0   0 0 1 0 0 0 0 0 2 0   0 0 0 0 0 0 0 3 0 0   0 0 0 1 2 2 3 2 2 2   3 2 0 0 0 2 2 2 0 0  1 xsize collect
    1 0 0 0 0 0 0 0 0 0   0 0 1 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0 0 0   0 0 0 1 2 2 2 2 2 2   2 2 0 0 0 0 0 0 0 0  1 xsize collect
    1 1 1 1 1 1 1 1 1 1   1 1 1 1 1 1 1 1 1 1   1 1 1 1 1 0 0 0 0 0   0 0 0 1 1 1 1 1 1 1   1 1 1 1 1 1 1 1 1 1  1 xsize collect
    0 0 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0 0 1   0 0 0 0 0 0 0 0 0 0   0 0 0 1 0 0 0 0 0 0   0 0 0 0 0 0 0 0 0 0  1 xsize collect
    0 0 0 0 0 0 0 2 0 0   0 0 0 0 0 0 0 0 0 1   0 0 2 0 0 0 0 0 3 0   0 0 0 0 0 0 0 3 3 0   0 0 0 0 0 0 0 0 0 0  1 xsize collect
    0 0 0 0 3 0 0 0 0 0   0 0 0 0 0 0 0 0 0 1   0 0 0 2 0 0 0 0 0 0   0 0 0 0 0 0 3 0 0 3   3 3 0 0 0 0 3 3 0 3  1 xsize collect
    0 0 0 0 0 0 0 0 0 0   0 0 0 0 0 2 0 0 0 1   0 0 0 0 0 0 0 0 0 0   0 0 0 0 3 3 2 2 0 0   0 0 3 3 3 3 0 0 3 0  1 xsize collect
    0 0 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0 0 1   0 0 2 0 0 0 0 0 0 0   0 0 0 1 0 2 2 2 2 2   0 0 0 0 0 0 0 0 0 0  1 xsize collect
    1 1 1 1 1 0 0 0 0 0   0 0 1 0 0 0 0 0 0 1   1 1 1 1 1 1 1 1 1 1   1 1 1 1 1 1 1 1 1 1   1 1 1 1 1 1 1 1 1 1  1 xsize collect
    0 0 0 0 0 0 0 0 0 0   0 0 1 0 0 0 0 0 0 0   0 0 0 0 0 1 2 3 3 0   2 0 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0 0 0  0 xsize collect
    0 0 0 0 0 0 0 0 0 0   0 0 1 0 0 0 0 0 0 0   0 0 0 0 0 1 3 2 2 3   2 0 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0 0 0  0 xsize collect
    0 0 0 2 0 0 0 0 0 0   0 0 1 0 0 3 0 0 0 0   0 2 2 0 0 1 2 3 0 2   0 0 0 0 0 3 0 0 0 0   0 0 0 0 0 0 0 0 0 0  0 xsize collect
    0 0 0 0 0 0 0 0 0 0   0 0 1 0 0 0 0 0 0 0   0 2 2 2 0 1 3 2 3 0   0 0 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0 0 0  0 xsize collect
    0 0 0 0 0 0 0 0 0 0   0 0 1 0 0 0 0 0 0 0   2 2 2 2 0 1 2 2 0 0   0 0 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0 0 0  0 xsize collect
    1 1 1 1 1 1 1 1 1 1   1 1 1 1 1 1 1 1 1 1   1 1 1 1 1 1 1 1 1 1   1 1 1 1 1 1 1 1 1 1   1 1 1 1 1 1 0 0 0 1  1 xsize collect

    ysize collect global map

    game
end

func wrapcoords do  // x, y
    dup 0 <      if drop ysize 1 - end
    dup ysize >= if drop 0         end
    swap
    dup 0 <      if drop xsize 1 - end
    dup xsize >= if drop 0         end
    swap
end

func gettile do  // x, y
    map swap index swap index
end

func settile do  // x, y, value
    store value
    store y
    store x
    map expand drop ysize 1 - y = ! if ysize y - pull end
    expand drop     xsize 1 - x = ! if xsize x - pull end
    drop value
    xsize 1 - x = ! if xsize x - 1 - push end xsize collect
    ysize 1 - y = ! if ysize y - 1 - push end ysize collect
    update map
end

func draw do
    0 store y
    ""
    y ysize < while
        0 store x
        x xsize < while
            x xpos = y ypos = & if "[]" end
            else
                x y gettile
                dup 0 = if ".." swap end
                dup 1 = if "##" swap end
                dup 2 = if "@@" swap end
                dup 3 = if "<>" swap end
                dup 4 = if x y 5 settile "**" swap end
                dup 5 = if x y 6 settile "^^" swap end
                dup 6 = if x y 0 settile "''" swap end
                dup 14 = if x y 4 settile "**" swap end
                dup 17 = if x y 7 settile "><" swap end
                // has to be last
                dup 7 = if x y   dobomb "><" swap end
                drop
            end
            +
            x 1 + update x
            x xsize <
        end
        "\n" +
        y 1 + update y
        y ysize <
    end
    "\n " + name + " hp: [" + "|" hp int * + "-" maxhp hp - * +
    "]    coins: " + coins types :str +
    0 0 os :cmdcurpos
    outln
end

func game do
    "cls" os :system drop
    title
    "\n\nEnter adventurer's name: " + in global name
    draw
    true while
        getaction dup 0 >= if
            xpos store xnew
            ypos store ynew
            dup 0 = if ypos 1 - update ynew end  // up
            dup 1 = if ypos 1 + update ynew end  // down
            dup 2 = if xpos 1 - update xnew end  // left
            dup 3 = if xpos 1 + update xnew end  // right
            xnew ynew wrapcoords update ynew update xnew
            xnew ynew gettile 1 = ! if
                xnew update xpos
                ynew update ypos
            end
        end
        drop
        xpos ypos gettile
        dup 2 = if
            coins 1 + update coins
            xpos ypos 0 settile
        end
        dup 3 = if
            xpos ypos 7 settile
            hp 1 - update hp
        end
        3 > if
            hp 1 - update hp
        end
        draw
        hp 0 <= if
            0 0 os :cmdcurpos
            "cls" os :system drop
            title
            "\n\nYou died! Press space/enter to restart!\n\n" +
            "And so the adventure of " + name + " ends...\n" +
            "Gold picked up: " + coins types :str + outln
            true while
                inch expand drop dup
                dup 3 = if 0 exit end  // exit on Crtl+C
                13 = swap 32 = | !
            end
            return
        end
        true
    end
end

func dobomb do  // x, y
    store y
    store x
    x     y 1 - bomb
    x     y     bomb
    x     y 1 + bombd
    x 1 - y 1 - bomb
    x 1 - y     bomb
    x 1 - y 1 + bombd
    x 1 + y 1 - bomb
    x 1 + y     bombd
    x 1 + y 1 + bombd
end

func bomb do  // x, y
    store y
    store x
    x y wrapcoords gettile 3 = if
        x y wrapcoords 7 settile
    end
    else
        x y wrapcoords 4 settile
    end
end

// "bomb down"
func bombd do  // x, y
    store y
    store x
    x y wrapcoords gettile 3 = if
        x y wrapcoords 17 settile
    end
    else
        x y wrapcoords 14 settile
    end
end

// attention, this inout doesnt work in pycharm, execute in normal console instead!
true while
    start
    true
end