#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <netdb.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#include "network.h"

int create_listen_socket(int port) {
    int sockfd = socket(AF_INET6, SOCK_STREAM, 0);
    if (sockfd < 0) {
        perror("socket");
        exit(1);
    }

    int enable = 1;
    setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &enable, sizeof(int));

    struct sockaddr_in6 addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin6_family = AF_INET6;
    addr.sin6_addr = in6addr_any;
    addr.sin6_port = htons(port);

    if (bind(sockfd, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        perror("bind");
        exit(1);
    }

    if (listen(sockfd, 10) < 0) {
        perror("listen");
        exit(1);
    }

    return sockfd;
}

int connect_to_host(const char *host, const char *port) {
    struct addrinfo hints = {0}, *res;
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    if (getaddrinfo(host, port, &hints, &res) != 0) {
        perror("getaddrinfo");
        return -1;
    }

    int sockfd = socket(res->ai_family, res->ai_socktype, res->ai_protocol);
    if (sockfd < 0 || connect(sockfd, res->ai_addr, res->ai_addrlen) < 0) {
        perror("connect");
        freeaddrinfo(res);
        return -1;
    }

    freeaddrinfo(res);
    return sockfd;
}