#ifndef LOG_H
#define LOG_H

#include <stddef.h>

void log_accepted();
void log_request_tail(const char *request);
void log_getting(const char *host, const char *uri);
void log_response_length(size_t length);

#endif