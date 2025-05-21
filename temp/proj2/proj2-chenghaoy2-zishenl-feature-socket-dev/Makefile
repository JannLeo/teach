CC = gcc
CFLAGS = -Wall -g
OBJ = main.o proxy.o log.o network.o
TARGET = htproxy

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJ)

main.o: main.c proxy.h
proxy.o: proxy.c proxy.h log.h network.h
log.o: log.c log.h
network.o: network.c network.h

clean:
	rm -f *.o *.log $(TARGET)