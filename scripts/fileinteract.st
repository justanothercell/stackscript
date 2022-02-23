"std.io" import store io

func test_w do
    "writing to file..." outln

    "/testing2.txt" io :file_write_create io :openfile store myfile
    "hello world" myfile :write
    myfile :close

    "wrote to file!" outln
end

func test_r do
    "\nreading from file...\n" outln

    "/testing.txt" io :file_read io :openfile store myfile
    myfile :read outln
    myfile :close

    "\nread from file!" outln
end

func test_a do
    "/testing2.txt" io :file_write_create_append io :openfile store myfile
    "Next user:\n\n" myfile :write
    "name: " dup in + "\n" + myfile :write
    "last name: " dup in + "\n" + myfile :write
    "age: " dup in + "\n\n" + myfile :write
    myfile :close
end

//test_w
//test_r

test_w

