#include <stdio.h>
#include <string.h>
#include "log.h"

void log_accepted() {
    printf("Accepted\n");
    fflush(stdout);
}

void log_request_tail(const char *request) {
    const char *tail = NULL;
    const char *line = request;
    while ((line = strstr(line, "\r\n")) != NULL) {
        const char *next = line + 2;
        if (*next == '\r' || *next == '\n' || *next == '\0') break;
        tail = next;
        line = next;
    }
    if (tail) {
        const char *end = strstr(tail, "\r\n");
        if (end) {
            printf("Request tail %.*s\n", (int)(end - tail), tail);
        } else {
            printf("Request tail %s\n", tail);
        }
    } else {
        printf("Request tail \n");
    }
    fflush(stdout);
}

void log_getting(const char *host, const char *uri) {
    printf("GETting %s %s\n", host, uri);
    fflush(stdout);
}

void log_response_length(size_t length) {
    printf("Response body length %zu\n", length);
    fflush(stdout);
}