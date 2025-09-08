// helloworld_syscall.c
char msg[] = "Hello world from shellcode!\n";

void _start() {
    asm(
        "mov $1, %%rax\n"        // syscall: write
        "mov $1, %%rdi\n"        // fd = stdout
        "lea msg(%%rip), %%rsi\n"// buffer address
        "mov $25, %%rdx\n"       // length
        "syscall\n"
        "mov $60, %%rax\n"       // syscall: exit
        "xor %%rdi, %%rdi\n"     // status = 0
        "syscall\n"
        :
        :
        : "rax","rdi","rsi","rdx"
    );
}
