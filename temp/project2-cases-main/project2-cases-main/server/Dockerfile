FROM golang:1-bookworm AS builder
WORKDIR /app
COPY server.go /app/server.go
RUN go build -ldflags "-s -w" -o /app/server /app/server.go

WORKDIR /staging
RUN mkdir -p /staging/usr/bin /staging/etc/nginx && cp /app/server /staging/usr/bin
COPY nginx.conf /staging/etc/nginx/nginx.conf
COPY supervisord.conf /staging/supervisord.conf

FROM ubuntu:22.04
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -yy --no-install-recommends \
        nginx supervisor \
    && useradd -u 1000 -m app \
    && chown -R app:app /var/log/nginx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /staging /

CMD ["/usr/bin/supervisord", "-c", "/supervisord.conf"]
