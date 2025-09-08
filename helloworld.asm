section .text
global _start

_start:
    mov rax, 1          ; syscall: write
    mov rdi, 1          ; fd = stdout
    lea rsi, [rel msg]  ; address of string inline in shellcode
    mov rdx, 25         ; length
    syscall
    mov rax, 60         ; exit
    xor rdi, rdi
    syscall

msg:
    db "Hello world from shellcode!",10
