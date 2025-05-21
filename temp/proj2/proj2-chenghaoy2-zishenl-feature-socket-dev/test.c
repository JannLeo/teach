#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <netdb.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

int create_listen_socket(char* port) {
    int sockfd, s;
    struct addrinfo hints, *res, *p;

    memset(&hints, 0, sizeof hints);
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags = AI_PASSIVE;

    s = getaddrinfo(NULL, port, &hints, &res);
    if (s != 0) {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(s));
        exit(EXIT_FAILURE);
    }

    for (p = res; p != NULL; p = p->ai_next) {
        sockfd = socket(p->ai_family, p->ai_socktype, p->ai_protocol);
        if (sockfd < 0) continue;

        int enable = 1;
        if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &enable, sizeof(int)) < 0) {
            perror("setsockopt");
            exit(EXIT_FAILURE);
        }

        if (bind(sockfd, p->ai_addr, p->ai_addrlen) == 0) break;

        close(sockfd);
    }

    if (p == NULL) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    if (listen(sockfd, 10) < 0) {
        perror("listen");
        exit(EXIT_FAILURE);
    }

    freeaddrinfo(res);
    return sockfd;
}

int create_client_socket(char* host, char* port) {
    int sockfd, s;
    struct addrinfo hints, *servinfo, *rp;

    memset(&hints, 0, sizeof hints);
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    s = getaddrinfo(host, port, &hints, &servinfo);
    if (s != 0) {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(s));
        exit(EXIT_FAILURE);
    }

    for (rp = servinfo; rp != NULL; rp = rp->ai_next) {
        sockfd = socket(rp->ai_family, rp->ai_socktype, rp->ai_protocol);
        if (sockfd == -1) continue;

        if (connect(sockfd, rp->ai_addr, rp->ai_addrlen) != -1)
            break;

        close(sockfd);
    }

    if (rp == NULL) {
        fprintf(stderr, "client: failed to connect\n");
        exit(EXIT_FAILURE);
    }

    freeaddrinfo(servinfo);
    return sockfd;
}

int find_last_line_start(char request[], int req_len) {
    for (int i = req_len - 4; i >= 1; i--) {
        if (request[i] == '\n' && request[i - 1] == '\r') {
            return i + 1;
        }
    }
    return 0;
}

int main(int argc, char** argv) {
    if (argc < 3 || strcmp(argv[1], "-p") != 0) {
        fprintf(stderr, "Usage: %s -p <listen-port>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    char* port = argv[2];
    int sockfd = create_listen_socket(port);

    while (1) {
        struct sockaddr_storage client_addr;
        socklen_t addr_size = sizeof(client_addr);
        int newsockfd = accept(sockfd, (struct sockaddr*)&client_addr, &addr_size);
        if (newsockfd < 0) {
            perror("accept");
            continue;
        }

        printf("Accepted\n");
        fflush(stdout);

        // 读取完整请求直到 \r\n\r\n
        char request[8192];
        int req_len = 0;
        char prev4[4] = {0};
        char c;
        while (read(newsockfd, &c, sizeof(c)) > 0) {
            request[req_len++] = c;
            memmove(prev4, prev4 + 1, 3);
            prev4[3] = c;
            if (memcmp(prev4, "\r\n\r\n", 4) == 0) break;
            if (req_len >= sizeof(request)) break;
        }

        int start = find_last_line_start(request, req_len);
        int end = req_len - 4;
        if (request[end - 1] == '\r') end--;

        printf("Request tail: ");
        for (int i = start; i < end; i++) {
            putchar(request[i]);
        }
        putchar('\n');
        fflush(stdout);

        request[req_len] = '\0';

        // 找 Host 字段
        char* hostline = NULL;
        char* req_copy = strdup(request);
        char* line = strtok(req_copy, "\r\n");
        while (line != NULL) {
            if (strncasecmp(line, "Host: ", 6) == 0) {
                hostline = line;
                break;
            }
            line = strtok(NULL, "\r\n");
        }

        if (!hostline) {
            fprintf(stderr, "Host not found\n");
            close(newsockfd);
            free(req_copy);
            continue;
        }

        char* host_start = hostline + 6;
        char host[256];
        int i = 0;
        while (host_start[i] != '\0' && host_start[i] != '\r' && i < sizeof(host) - 1) {
            host[i] = host_start[i];
            i++;
        }
        host[i] = '\0';
        free(req_copy);

        // 提取 URI
        int uri_start = 0;
        for (i = 0; i < req_len; i++) {
            if (request[i] == ' ') {
                uri_start = i + 1;
                break;
            }
        }

        char uri[256];
        int count = 0;
        for (i = uri_start; i < req_len && count < sizeof(uri) - 1; i++) {
            if (request[i] != ' ') {
                uri[count++] = request[i];
            } else {
                break;
            }
        }
        uri[count] = '\0';

        printf("GETting localhost %s\n", uri);
        fflush(stdout);

        // 转发请求
        int server_fd = create_client_socket(host, "80");
        int sent = 0;
        while (sent < req_len) {
            int n = write(server_fd, request + sent, req_len - sent);
            if (n <= 0) break;
            sent += n;
        }

        // 读取响应
        int total_bytes = 0;
        int n;
        while ((n = read(server_fd, &c, sizeof(c))) > 0) {
            total_bytes += n;
            write(newsockfd, &c, n);
        }
        printf("read() finished, total_bytes = %d\n", total_bytes);
        fflush(stdout);

        close(server_fd);
        close(newsockfd);
    }

    close(sockfd);
    return 0;
}
