#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <err.h>
#include <stdint.h>
#include <errno.h>
#include <string.h>
#include <dev/pci/p6statsvar.h>

void usage(const char *prog) {
    fprintf(stderr, "Usage: %s [-r] [-w] [-n] [numbers...]\n", prog);
    fprintf(stderr, "  -r  mode read\n");
    fprintf(stderr, "  -w  mode write\n");
    fprintf(stderr, "  -n  non-blocking\n");
    exit(1);
}

int main(int argc, char *argv[]) {
    int fd;
    int opt;
    int mode_read = 0, mode_write = 0, nonblock = 0;
    uint64_t arr[256];
    int arr_len = 0;

    while ((opt = getopt(argc, argv, "rwn")) != -1) {
        switch (opt) {
            case 'r': mode_read = 1; break;
            case 'w': mode_write = 1; break;
            default: usage(argv[0]);
        }
    }

    if (!mode_read && !mode_write) {
        mode_read = mode_write = 1;
    }

    for (int i = optind; i < argc; i++) {
        if (arr_len >= P6_R_ICOUNT_MAX) {
            fprintf(stderr, "Too many numbers, max %d\n", P6_R_ICOUNT_MAX);
            exit(1);
        }
        arr[arr_len++] = strtoull(argv[i], NULL, 10);
    }

    if (mode_write && arr_len == 0) {
        fprintf(stderr, "No numbers provided for write\n");
        usage(argv[0]);
    }

    int flags = (mode_read && mode_write) ? O_RDWR : 
                (mode_read ? O_RDONLY : O_WRONLY);
    if (nonblock) flags |= O_NONBLOCK;
    
    fd = open("/dev/p6stats", flags);
    if (fd < 0)
        err(1, "open");

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