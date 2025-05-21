#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "proxy.h"

int main(int argc, char **argv) {
    if (argc < 3 || strcmp(argv[1], "-p") != 0) {
        fprintf(stderr, "Usage: %s -p <listen-port> [-c]\n", argv[0]);
        exit(1);
    }

    int port = atoi(argv[2]);
    int enable_cache = (argc == 4 && strcmp(argv[3], "-c") == 0);

    start_proxy_server(port, enable_cache);
    return 0;
}