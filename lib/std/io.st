"std.os" import store os

os :O_CREAT store file_create
os :O_RDONLY store file_read
os :O_WRONLY store file_write
os :O_WRONLY os :O_CREAT | store file_write_create
os :O_WRONLY os :O_APPEND | store file_write_append
os :O_WRONLY os :O_APPEND os :O_CREAT | | store file_write_create_append
os :O_RDWR store file_read_write
os :O_RDWR os :O_CREAT | store file_read_write_create


func openfile do // [filepath, mode]
    swap abspath swap
    "std.io.file" import dup 3 push :_open
end

func abspath do
    dup 0 index "/" = if
        os :getcwd swap +
    end
end
