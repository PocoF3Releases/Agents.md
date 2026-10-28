#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <signal.h>
#include <poll.h>
#include <sys/wait.h>
#include <sys/ioctl.h>
#include <sys/mman.h>
#define __user
#include "msm_kgsl.h"
/* Exercise fd/process teardown, not explicit object-free ioctls. */
static int worker(int pipefd, int killed) {
    int fd = open("/dev/kgsl-3d0", O_RDWR | O_CLOEXEC);
    if (fd < 0)
        return 1;
    struct kgsl_drawctxt_create ctx = {.flags = KGSL_CONTEXT_PREAMBLE | KGSL_CONTEXT_NO_GMEM_ALLOC};
    if (ioctl(fd, IOCTL_KGSL_DRAWCTXT_CREATE, &ctx))
        return 2;
    for (int i = 0; i < 8; i++) {
        struct kgsl_gpumem_alloc_id m = {.size = 1024 * 1024};
        if (ioctl(fd, IOCTL_KGSL_GPUMEM_ALLOC_ID, &m))
            return 3;
        void *ptr =
            mmap(NULL, m.mmapsize, PROT_READ | PROT_WRITE, MAP_SHARED, fd, (off_t)m.id * 4096);
        if (ptr == MAP_FAILED)
            return 4;
        ((volatile unsigned char *)ptr)[0] = 0x5a;
        ((volatile unsigned char *)ptr)[1024 * 1024 - 1] = 0xa5;
    }
    struct kgsl_timeline_create t = {.seqno = 1};
    if (ioctl(fd, IOCTL_KGSL_TIMELINE_CREATE, &t))
        return 5;
    struct kgsl_timeline_fence_get f = {.timeline = t.id, .seqno = 2, .handle = -1};
    if (ioctl(fd, IOCTL_KGSL_TIMELINE_FENCE_GET, &f) || f.handle < 0)
        return 6;
    if (write(pipefd, "R", 1) != 1)
        return 7;
    close(pipefd);
    if (killed) {
        alarm(10);
        for (;;)
            pause();
    }
    usleep(200000);
    return 0;
}
int main(void) {
    setvbuf(stdout, NULL, _IOLBF, 0);
    int failures = 0;
    for (int round = 0; round < 8; round++) {
        pid_t pid[4];
        int pipes[4][2];
        for (int i = 0; i < 4; i++) {
            if (pipe(pipes[i]))
                return 10;
            pid[i] = fork();
            if (pid[i] < 0)
                return 11;
            if (!pid[i]) {
                close(pipes[i][0]);
                _exit(worker(pipes[i][1], round & 1));
            }
            close(pipes[i][1]);
        }
        for (int i = 0; i < 4; i++) {
            struct pollfd pf = {.fd = pipes[i][0], .events = POLLIN};
            char ready = 0;
            int good = poll(&pf, 1, 5000) > 0 && read(pf.fd, &ready, 1) == 1 && ready == 'R';
            close(pf.fd);
            if (!good) {
                failures++;
                kill(pid[i], SIGKILL);
            } else if (round & 1)
                kill(pid[i], SIGKILL);
            int status;
            if (waitpid(pid[i], &status, 0) != pid[i])
                return 12;
            int pass = good && ((round & 1) ? (WIFSIGNALED(status) && WTERMSIG(status) == SIGKILL)
                                            : (WIFEXITED(status) && WEXITSTATUS(status) == 0));
            if (!pass)
                failures++;
            printf("%s round=%d worker=%d pid=%d mode=%s\n", pass ? "PASS" : "FAIL", round, i,
                   pid[i], (round & 1) ? "SIGKILL" : "exit");
        }
        usleep(100000);
    }
    printf("SUMMARY teardown=32 failures=%d\n", failures);
    return failures ? 1 : 0;
}
