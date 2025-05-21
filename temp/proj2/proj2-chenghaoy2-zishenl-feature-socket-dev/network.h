#ifndef NETWORK_H
#define NETWORK_H

int create_listen_socket(int port);
int connect_to_host(const char *host, const char *port);

#endif