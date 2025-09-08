#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <err.h>
#include <string.h>
#include <strings.h>
#include <limits.h>

#include <sys/fcntl.h>
#include <sys/limits.h>

#include <sys/p5d.h>

static void
usage(void)
{
    fprintf(stderr, "usage: xnum -r\n"
        "       xnum -s NUMBER\n"
        "       xnum -t\n");
    exit(1);
}

int
main(int argc, char *argv[])
{
    int ch;
    int fd;
    enum { NONE, SEND, RECEIVE, CHECK } mode = NONE;
    int num;
    const char *errstr;
    struct p5d_status_params stp;

    while ((ch = getopt(argc, argv, "rs:t")) != -1) {
        switch (ch) {
        case 't':
            if (mode != NONE) {
                warnx("only one of -rst may be given");
                usage();
            }
            mode = CHECK;
            break;
        case 'r':
            if (mode != NONE) {
                warnx("only one of -rst may be given");
                usage();
            }
            mode = RECEIVE;
            break;
        case 's':
            if (mode != NONE) {
                warnx("only one of -rst may be given");
                usage();
            }
            mode = SEND;
            num = strtonum(optarg, 0, INT32_MAX, &errstr);
            if (errstr != NULL) {
                warnx("-s number is %s: %s", errstr, optarg);
                usage();
            }
            break;
        default:
            usage();
        }
    }
    argc -= optind;
    if (argc > 0)
        usage();

    fd = open("/dev/p5d", O_RDWR);
    if (fd < 0)
        err(1, "open");

    switch (mode) {
    case NONE:
        warnx("one of -rst must be given");
        usage();

    case CHECK:
        bzero(&stp, sizeof(stp));
        if (ioctl(fd, P5D_IOC_STATUS, &stp))
            err(1, "ioctl(P5D_IOC_STATUS)");
        if (stp.psp_is_num_waiting) {
            printf("yes\n");
            exit(0);
        } else {
            printf("no\n");
            exit(1);
        }

    case SEND:
        if (write(fd, &num, sizeof(num)) < 0)
            err(1, "write");
        return (0);

    case RECEIVE:
        if (read(fd, &num, sizeof(num)) < 0)
            err(1, "read");
        printf("%d\n", num);
        return (0);
    }

}