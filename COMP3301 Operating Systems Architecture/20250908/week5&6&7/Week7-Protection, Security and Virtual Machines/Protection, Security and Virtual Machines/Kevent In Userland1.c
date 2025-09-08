#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <err.h>
#include <stdint.h>
#include <errno.h>
#include <string.h>
#include <sys/event.h>
#include <sys/types.h>
#include <sys/time.h>

#include <dev/pci/p6statsvar.h>

void usage(const char *prog) {
    fprintf(stderr, "Usage: %s [-r] [-w] [-n] [-R] [-W] [numbers...]\n", prog);
    fprintf(stderr, "  -r  read only\n");
    fprintf(stderr, "  -w  write only (requires at least one number)\n");
    fprintf(stderr, "  -n  non-blocking\n");
    fprintf(stderr, "  -R  check if read is ready\n");
    fprintf(stderr, "  -W  check if write is ready\n");
    exit(1);
}

int main(int argc, char *argv[]) {
    int fd, kq;
    int opt;
    int mode_read = 0, mode_write = 0, nonblock = 0;
    int check_read = 0, check_write = 0;
    uint64_t arr[256];
    int arr_len = 0;

    while ((opt = getopt(argc, argv, "rwnRW")) != -1) {
        switch (opt) {
            case 'r': mode_read = 1; break;
            case 'w': mode_write = 1; break;
            case 'n': nonblock = 1; break;
            case 'R': check_read = 1; break;
            case 'W': check_write = 1; break;
            default: usage(argv[0]);
        }
    }

    // Error if neither read nor write requested
    if (!mode_read && !mode_write && !(check_read || check_write)) {
        fprintf(stderr, "Error: Must specify at least -r or -w (or -R/-W for readiness check)\n");
        usage(argv[0]);
    }

    // Collect numbers for writing if -w is passed
    if (mode_write) {
        for (int i = optind; i < argc; i++) {
            if (arr_len >= 256) {
                fprintf(stderr, "Too many numbers, max 256\n");
                exit(1);
            }
            arr[arr_len++] = strtoull(argv[i], NULL, 10);
        }
        if (arr_len == 0) {
            fprintf(stderr, "Write mode requires at least one number\n");
            usage(argv[0]);
        }
    }

    int flags = 0;
    if (mode_read && mode_write) flags = O_RDWR;
    else if (mode_read) flags = O_RDONLY;
    else if (mode_write) flags = O_WRONLY;

    if (nonblock) flags |= O_NONBLOCK;

    printf("0x%x\r\n", flags);

    fd = open("/dev/p6stats", flags);
    if (fd < 0)
        err(1, "open");

if (check_read || check_write) {
    kq = kqueue();
    if (kq < 0) err(1, "kqueue");

    struct kevent ev_set[2];
    struct kevent ev_list[2];
    int n = 0;

    if (check_read)
        EV_SET(&ev_set[n++], fd, EVFILT_READ, EV_ADD | EV_ENABLE, 0, 0, NULL);
    if (check_write)
        EV_SET(&ev_set[n++], fd, EVFILT_WRITE, EV_ADD | EV_ENABLE, 0, 0, NULL);

    // Register events
    if (kevent(kq, ev_set, n, NULL, 0, NULL) < 0)
        err(1, "kevent register");

    // Check readiness with zero timeout
    struct timespec ts = {0, 0};
    int nev = kevent(kq, NULL, 0, ev_list, n, &ts);
    if (nev < 0) err(1, "kevent wait");

    for (int i = 0; i < nev; i++) {
        if (ev_list[i].filter == EVFILT_READ)
            printf("Read is ready\n");
        if (ev_list[i].filter == EVFILT_WRITE)
            printf("p6stats device ready for input\n");
    }

    // If no events returned, report busy / not ready
    if (nev == 0) {
        if (check_read) printf("No read is ready\n");
        if (check_write) printf("p6stats busy\n");
    }

    close(kq);
}

    if (mode_write) {
        ssize_t rc = write(fd, arr, arr_len * sizeof(uint64_t));
        if (rc < 0) {
            if (errno == EBUSY)
                fprintf(stderr, "Write error: Device busy (non-blocking)\n");
            else
                fprintf(stderr, "Write error: %s\n", strerror(errno));
        } else {
            printf("Wrote %zd bytes\n", rc);
        }
    }

    if (mode_read) {
        struct p6stats_output out;
        ssize_t rc = read(fd, &out, sizeof(out));
        if (rc < 0) {
            if (errno == ENOMSG)
                fprintf(stderr, "Read error: No write has been made yet\n");
            else if (errno == EAGAIN)
                fprintf(stderr, "Read error: Device not done (non-blocking)\n");
            else
                fprintf(stderr, "Read error: %s\n", strerror(errno));
        } else {
            printf("count  = %llu\n", out.po_count);
            printf("sum    = %llu\n", out.po_sum);
            printf("mean   = %llu\n", out.po_mean);
            printf("median = %llu\n", out.po_median);
        }
    }

    close(fd);
    return 0;
}