#include "http.h"

#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <netinet/in.h>
#include <pthread.h>

void *client_thread(void *vptr) {
  int fd = (int)(ssize_t)vptr;

  // read an HTTP request from fd 
  HTTPRequest req;
  if (httprequest_read(&req, fd) < 0) {
    // Bad request or parse error; maybe close the socket and return
    close(fd);
    return NULL;
  }

  //get full file path
  const char *file_path = httprequest_get_path(&req); //file path
  if(strcmp(file_path, "/") == 0) {
    file_path = "/index.html";
  }
  //add static
  char filepath[1024];
  snprintf(filepath, sizeof(filepath), "static%s", file_path);

    /* try to open the file, if can't open(meaning file doesn't exists), 
    respond with 404 not found and then close(fd), destroy req and return NULL
    */
  FILE *fp = fopen(filepath, "rb");

  if(!fp) {
    // Send 404 Not Found
    dprintf(fd, "HTTP/1.1 404 Not Found\r\n");
    dprintf(fd, "Content-Length: 0\r\n");
    dprintf(fd, "\r\n");
    close(fd);
    httprequest_destroy(&req);
    return NULL;
  }

  //the file does exists : create a HTTP 200 OK packet response 
    //first get file size(using fseek) and content type(using )
    fseek(fp, 0, SEEK_END);
    long file_size = ftell(fp);
    fseek(fp, 0, SEEK_SET); //reset to front

    const char *content_type;
    if (strstr(file_path, ".html")) content_type = "text/html";
    else content_type = "image/png";

  dprintf(fd, "HTTP/1.1 200 OK\r\n");
  dprintf(fd, "Content-Length: %ld\r\n", file_size);
  dprintf(fd, "Content-Type: %s\r\n", content_type);
  dprintf(fd, "\r\n");

  //send file contents
  char buffer[8192];
  int n;
  while((n = fread(buffer, 1, 8192, fp)) > 0) {
    write(fd, buffer, n);
  }
  fclose(fp);

  httprequest_destroy(&req);
  close(fd);
  return NULL;
}

int main(int argc, char *argv[]) {
  if (argc != 2) {
    printf("Usage: %s <port>\n", argv[0]);
    return 1;
  }
  int port = atoi(argv[1]);
  printf("Binding to port %d. Visit http://localhost:%d/ to interact with your server!\n", port, port);

  // socket:
  int sockfd = socket(AF_INET, SOCK_STREAM, 0);

  // bind:
  struct sockaddr_in server_addr, client_address;
  memset(&server_addr, 0x00, sizeof(server_addr));
  server_addr.sin_family = AF_INET;
  server_addr.sin_addr.s_addr = INADDR_ANY;
  server_addr.sin_port = htons(port);  
  bind(sockfd, (const struct sockaddr *)&server_addr, sizeof(server_addr));

  // listen:
  listen(sockfd, 10);

  // accept:
  socklen_t client_addr_len;
  while (1) {
    client_addr_len = sizeof(struct sockaddr_in);
    int fd = accept(sockfd, (struct sockaddr *)&client_address, &client_addr_len);
    printf("Client connected (fd=%d)\n", fd);

    pthread_t tid;
    pthread_create(&tid, NULL, client_thread, (void *)(ssize_t)fd);
    pthread_detach(tid);
  }

  return 0;
}
