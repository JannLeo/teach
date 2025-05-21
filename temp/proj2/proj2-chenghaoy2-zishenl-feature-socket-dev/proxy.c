#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <netdb.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#include "proxy.h"
#include "log.h"
#include "network.h"

#define BUFFER_SIZE 8192
#define MAX_RESPONSE_SIZE (100 * 1024)

void rewrite_request_line(char *buffer) {
    char *first_crlf = strstr(buffer, "\r\n");
    if (!first_crlf) return;

    char request_line[1024] = {0};
    size_t line_len = first_crlf - buffer;
    strncpy(request_line, buffer, line_len);

    char method[16], full_uri[2048], version[32];
    sscanf(request_line, "%15s %2047s %31s", method, full_uri, version);

    const char *path = strchr(full_uri + 7, '/'); // skip "http://"
    if (!path) path = "/";

    char new_request[1024];
    snprintf(new_request, sizeof(new_request), "%s %s %s\r\n", method, path, version);

    // Append rest of the header starting from original buffer's CRLF
    char new_buffer[BUFFER_SIZE];
    snprintf(new_buffer, sizeof(new_buffer), "%s%s", new_request, first_crlf + 2);

    // Copy back to original buffer
    strncpy(buffer, new_buffer, BUFFER_SIZE - 1);
    buffer[BUFFER_SIZE - 1] = '\0';
}

void start_proxy_server(int port, int enable_cache) {
    int listen_fd = create_listen_socket(port);

    while (1) {
        int client_fd = accept(listen_fd, NULL, NULL);
        if (client_fd < 0) {
            perror("accept");
            continue;
        }

        log_accepted();

        char buffer[BUFFER_SIZE];
        ssize_t bytes_read = recv(client_fd, buffer, BUFFER_SIZE - 1, 0);
        if (bytes_read <= 0) {
            close(client_fd);
            continue;
        }
        buffer[bytes_read] = '\0';

        // Extract request tail line
        log_request_tail(buffer);

        // Extract URI and host from GET line directly
        char uri[2048] = {0};
        char host[256] = {0};

        char *get_line_end = strstr(buffer, "\r\n");
        if (get_line_end) {
            char get_line[1024] = {0};
            size_t len = get_line_end - buffer;
            strncpy(get_line, buffer, len);

            if (strncmp(get_line, "GET ", 4) == 0) {
                sscanf(get_line, "GET %s", uri);
                if (strncmp(uri, "http://", 7) == 0) {
                    const char *start = uri + 7;
                    const char *end = strchr(start, '/');
                    if (end) {
                        size_t host_len = end - start;
                        strncpy(host, start, host_len);
                        host[host_len] = '\0';
                    } else {
                        strncpy(host, start, 255);
                    }
                }
            }
        }

        log_getting(host, uri);

        // Rewrite request line to origin-form
        rewrite_request_line(buffer);

        int server_fd = connect_to_host(host, "80");
        if (server_fd < 0) {
            close(client_fd);
            continue;
        }

        send(server_fd, buffer, strlen(buffer), 0);

        // Relay response and count body length only
        char response[BUFFER_SIZE];
        size_t total_sent = 0;
        ssize_t rbytes;
        int header_parsed = 0;
        size_t body_start = 0;
        char *header_end = NULL;

        while ((rbytes = read(server_fd, response, BUFFER_SIZE)) > 0) {
            send(client_fd, response, rbytes, 0);

            if (!header_parsed) {
                header_end = strstr(response, "\r\n\r\n");
                if (header_end) {
                    header_parsed = 1;
                    body_start = header_end + 4 - response;
                    total_sent += rbytes - body_start;
                }
            } else {
                total_sent += rbytes;
            }

            if (total_sent > MAX_RESPONSE_SIZE) break;
        }

        log_response_length(total_sent);
        fflush(stdout);

        close(server_fd);
        close(client_fd);
    }
}
