#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdio.h>

#include "http.h"



//helper function

static char *trim_leading_spaces(char *str) {
    while (*str == ' ' || *str == '\t') {
        str++;
    }
    return str;
}




/**
 * httprequest_parse_headers
 * 
 * Populate a `req` with the contents of `buffer`, returning the number of bytes used from `buf`.
 */
ssize_t httprequest_parse_headers(HTTPRequest *req, char *buffer, ssize_t buffer_len) {
    char *buf_copy = malloc(buffer_len + 1);
    if (!buf_copy) {
        return -1;
    }
    memcpy(buf_copy, buffer, buffer_len);
    buf_copy[buffer_len] = '\0';
    //header_end
    char *header_end = strstr(buf_copy, "\r\n\r\n");
    if (!header_end) {
        free(buf_copy);
        return -1;
    }
    
    ssize_t headers_len = header_end - buf_copy + 4;
    char *payload_ptr = buf_copy + headers_len;

    char *headers_section = malloc(headers_len + 1);
    if (!headers_section) {
        free(buf_copy);
        return -1;
    }
    memcpy(headers_section, buf_copy, headers_len);
    headers_section[headers_len] = '\0';

    char *saveptr;
    char *line = strtok_r(headers_section, "\r\n", &saveptr);
    if (!line) {
        free(buf_copy);
        free(headers_section);
        return -1;
    }

    char *method = strtok(line, " ");
    char *path = strtok(NULL, " ");
    char *version = strtok(NULL, " ");
    if (!method || !path || !version) {
        free(buf_copy);
        free(headers_section);
        return -1;
    }
    
    req->action = strdup(method);
    req->path = strdup(path);
    req->version = strdup(version);
    req->payload = NULL;
    req->headers = NULL;

    if (!req->action || !req->path || !req->version) { // 确保所有 strdup() 都成功
        
        free(buf_copy);
        free(headers_section);
        httprequest_destroy(req);
        return -1;
    }

    int content_length = 0;
    while ((line = strtok_r(NULL, "\r\n", &saveptr)) != NULL) {
        char *colon = strchr(line, ':');
        if (!colon) {
            continue;
        }

        *colon = '\0';
        char *key = line;
        char *value = colon + 1;
        value = trim_leading_spaces(value);//this is the helper

        HeaderNode *node = malloc(sizeof(HeaderNode));
        if (!node) {
            
            free(buf_copy);
            
            free(headers_section);
            httprequest_destroy(req);
            return -1;
        }

        node->key = strdup(key);
        node->value = strdup(value);
        if (!node->key || !node->value) {  
            free(node->key);
            free(node->value);
            free(node);
            httprequest_destroy(req);
            free(buf_copy);
            free(headers_section);
            return -1;
        }

        node->next = req->headers;
        req->headers = node;

        if (strcasecmp(key, "Content-Length") == 0) {
            content_length = atoi(value);
        }
    }

    if (content_length > 0) {
        if (headers_len + content_length > buffer_len) {
            free(buf_copy);
            free(headers_section);
            httprequest_destroy(req);
            return -1;
        }

        char *temp_payload = malloc(content_length + 1);
        if (!temp_payload) {
            
            free(buf_copy);
            free(headers_section);
            httprequest_destroy(req);
            return -1;
        }

        memcpy(temp_payload, payload_ptr, content_length);
        temp_payload[content_length] = '\0';
        req->payload = temp_payload;
    }

    free(buf_copy);
    free(headers_section);
    return headers_len + content_length;
}





/**
 * httprequest_read
 * 
 * Populate a `req` from the socket `sockfd`, returning the number of bytes read to populate `req`.
 */
#define READ_BLOCK_SIZE 4096

ssize_t httprequest_read(HTTPRequest *req, int sockfd) {
    size_t capacity = 8192;//capicity size
    char *buffer = malloc(capacity);
    if (!buffer) {
        return -1; 
    }

    ssize_t total_read = 0;
    ssize_t parse_result = -1;

    while (1) {
        if ((size_t)total_read + READ_BLOCK_SIZE > capacity) {
            size_t new_capacity = capacity * 2;
            char *tmp = realloc(buffer, new_capacity);
            if (!tmp) {
                return -1; 
            }
            buffer = tmp;
            capacity = new_capacity;
        }
        ssize_t bytes_read = read(sockfd, buffer + total_read, READ_BLOCK_SIZE);
        if (bytes_read < 0) {
            free(buffer);
            return -1;
        }
        if (bytes_read == 0) {
            parse_result = httprequest_parse_headers(req, buffer, total_read);
            free(buffer);
            if (parse_result >= 0) {
                return total_read; 
            }
            return -1; 
        }
        total_read += bytes_read;
        parse_result = httprequest_parse_headers(req, buffer, total_read);
        if (parse_result >= 0) {
            free(buffer);
            return total_read;
        }
    }
    free(buffer);
    return -1;
}


/**
 * httprequest_get_action
 * 
 * Returns the HTTP action verb for a given `req`.
 */
const char *httprequest_get_action(HTTPRequest *req) {
  return req->action;
}


/**
 * httprequest_get_header
 * 
 * Returns the value of the HTTP header `key` for a given `req`.
 */
const char *httprequest_get_header(HTTPRequest *req, const char *key) {
  if (!req || !key) {
    return NULL;
  }
  HeaderNode *current = req->headers;
  while (current) {
    if (current->key && strcasecmp(current->key, key) == 0) {
      return current->value;
    }
      current = current->next;
    }
    return NULL;
}


/**
 * httprequest_get_path
 * 
 * Returns the requested path for a given `req`.
 */
const char *httprequest_get_path(HTTPRequest *req) {
  if (!req) {
    return NULL;
  }
  return req->path;
}


/**
 * httprequest_destroy
 * 
 * Destroys a `req`, freeing all associated memory.
 */
void httprequest_destroy(HTTPRequest *req) {
  if (!req) { 
    return;
  } 
  free((void *)req->action);
  free((void *)req->path);
  free((void *)req->version);
  free((void *)req->payload);
  HeaderNode *current = req->headers;
  while (current) {
    HeaderNode *next = current->next;
      if (current->key) {
        free(current->key);
      }  
      if (current->value) {
        free(current->value);
      }
      free(current);
      current = next;
    }
  req->headers = NULL;

}