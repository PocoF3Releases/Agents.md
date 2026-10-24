#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
static unsigned char b[4096],q[4096];
int main(void){const char *path="/data/local/tmp/codex-hardware-storage-canary.tmp";int fd=open(path,O_CREAT|O_EXCL|O_RDWR|O_CLOEXEC,0600);if(fd<0){perror("exclusive create");return 1;}int fail=0;for(unsigned n=0;n<2048;n++){for(unsigned i=0;i<sizeof(b);i++)b[i]=(n*17+i*29)^0x5a;if(write(fd,b,sizeof(b))!=(ssize_t)sizeof(b)){fail=1;break;}}if(fsync(fd))fail=1;close(fd);fd=open(path,O_RDONLY|O_CLOEXEC);if(fd<0)fail=1;else{for(unsigned n=0;n<2048;n++){for(unsigned i=0;i<sizeof(b);i++)b[i]=(n*17+i*29)^0x5a;if(read(fd,q,sizeof(q))!=(ssize_t)sizeof(q)||memcmp(b,q,sizeof(b))){fail=1;break;}}close(fd);}if(unlink(path))fail=1;printf("%s 8 MiB exclusive write/fsync/close/reopen/readback/cleanup\n",fail?"FAIL":"PASS");return fail;}
