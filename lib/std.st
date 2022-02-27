// lets you use all the standard modules as if having imported them one by one like this yourself
// only use "std" import drop in global context when you are sure this script is never called by another one, as
// it overrides these names which may have been already used.

"std.builtins" import global builtins
"std.math" import global math
"std.os" import global os
"std.types" import global types
"std.io" import global io
