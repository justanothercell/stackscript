"std.types" import store types
"std.os" import store os

"" store mode
"" store filepath
false store isopen
0 store fid

func _open do  // [filepath, mode]
    update mode
    update filepath
    filepath mode os :open update fid
    mode os :O_APPEND & 0 = if
        mode os :O_RDWR & mode os :O_WRONLY & | if
            fclear
        end
    end
    true update isopen
end

func close do  // []
    false update isopen
    fid os :close
end

func fclear do
    fid 0 os :ftruncate
end

func write do  // [str]
    'utf-8' types :encode writebytes
end

func writebytes do  // [bytes]
    fid swap os :write
end

func read do  // []
    readbytes 'utf-8' types :decode
end

func readbytes do  // []
    fid fsize os :read
end

func fsize do
    filepath os :stat 6 index
end