import ctypes

# This is safe demo data: a machine code function that just "return 42".
# (x86_64 Linux, mov eax, 42; ret)
# Bytes: b8 2a 00 00 00 c3
#code = b"\xb8\x2a\x00\x00\x00\xc3"
#code = b"\xf3\x0f\x1e\xfa\x48\xc7\xc0\x01\x00\x00\x00\x48\xc7\xc7\x01\x00\x00\x00\x48\x8d\x35\xe7\x2f\x00\x00\x48\xc7\xc2\x19\x00\x00\x00\x0f\x05\x48\xc7\xc0\x3c\x00\x00\x00\x48\x31\xff\x0f\x05\xc3"
code = b"\xb8\x01\x00\x00\x00\xbf\x01\x00\x00\x00\x48\x8d\x35\x11\x00\x00\x00\xba\x19\x00\x00\x00\x0f\x05\xb8\x3c\x00\x00\x00\x48\x31\xff\x0f\x05\x48\x65\x6c\x6c\x6f\x20\x77\x6f\x72\x6c\x64\x20\x66\x72\x6f\x6d\x20\x73\x68\x65\x6c\x6c\x63\x6f\x64\x65\x21\x0a"
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
