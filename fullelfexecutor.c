#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/syscall.h>
#include <fcntl.h>
#include <string.h>
#include <errno.h>

// Include your ELF bytes here (e.g., generated with xxd -i)
#include "helloworld_hex.c"  // contains unsigned char helloworld[] and unsigned int sizeof(helloworld_elf)

int main() {
    // 1. Create anonymous memory file descriptor
    int fd = syscall(SYS_memfd_create, "inmem_elf", MFD_CLOEXEC);
    if (fd == -1) {
        perror("memfd_create failed");
        return 1;
    }

    // 2. Write ELF bytes to memfd
    ssize_t written = write(fd, helloworld_elf, sizeof(helloworld_elf));
    if (written != sizeof(helloworld_elf)) {
        perror("write to memfd failed");
        close(fd);
        return 1;
    }

    // 3. Reset file offset to beginning
    if (lseek(fd, 0, SEEK_SET) == -1) {
        perror("lseek failed");
        close(fd);
        return 1;
    }

    // 4. Execute ELF directly from memfd
    char *const argv[] = {NULL};
    char *const envp[] = {NULL};

    if (fexecve(fd, argv, envp) == -1) {
        perror("fexecve failed");
        close(fd);
        return 1;
    }

    close(fd);
    return 0;
}
