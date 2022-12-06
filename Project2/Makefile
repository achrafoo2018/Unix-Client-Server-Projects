CC = gcc
CFLAGS = -Wall -g
LDFLAGS = -lpthread

all: Server Client

Server: Server.c
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

Client: Client.c
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

clean:
	rm -f Server Client

