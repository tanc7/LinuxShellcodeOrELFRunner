import ctypes

# This is safe demo data: a machine code function that just "return 42".
# (x86_64 Linux, mov eax, 42; ret)
# Bytes: b8 2a 00 00 00 c3
code = b"\xb8\x2a\x00\x00\x00\xc3"

# Allocate executable memory
PROT_READ = 1
PROT_WRITE = 2
PROT_EXEC = 4
MAP_PRIVATE = 2
MAP_ANON = 0x20

libc = ctypes.CDLL(None)
mmap = libc.mmap
mmap.restype = ctypes.c_void_p
addr = mmap(
    None,
    len(code),
    PROT_READ | PROT_WRITE | PROT_EXEC,
    MAP_PRIVATE | MAP_ANON,
    -1,
    0,
)

# Copy bytes into the allocated region
ctypes.memmove(addr, code, len(code))

# Cast memory to a function pointer type: int func(void)
func_type = ctypes.CFUNCTYPE(ctypes.c_int)
func = func_type(addr)

# Call it
result = func()
print("Function returned:", result)
