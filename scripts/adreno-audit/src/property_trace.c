#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdarg.h>
#include <stdio.h>
#include <errno.h>
#include <stdint.h>
#include <sys/ioctl.h>
struct prop {
    unsigned int type;
    void *value;
    size_t sizebytes;
};
static int (*real_ioctl)(int, int, ...);
__attribute__((constructor)) static void init(void) { real_ioctl = dlsym(RTLD_NEXT, "ioctl"); }
int ioctl(int fd, int request, ...) {
    va_list ap;
    va_start(ap, request);
    void *arg = va_arg(ap, void *);
    va_end(ap);
    if (!real_ioctl) {
        errno = ENOSYS;
        return -1;
    }
    int rc = real_ioctl(fd, request, arg);
    int saved = errno;
    if (_IOC_TYPE(request) == 9 && _IOC_NR(request) == 2 && arg) {
        struct prop *p = arg;
        fprintf(stderr, "KGSL_PROPERTY type=0x%x size=%zu rc=%d errno=%d\n", p->type, p->sizebytes,
                rc, rc < 0 ? saved : 0);
    }
    errno = saved;
    return rc;
}
