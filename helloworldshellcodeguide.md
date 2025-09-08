nasm -f elf64 helloworld.asm -o helloworld.o
ld -o helloworld.elf helloworld.o
objcopy -O binary --only-section=.text helloworld.elf helloworld.bin
xxd -p helloworld.bin | tr -d '\n' | sed 's/\(..\)/\\x\1/g'
