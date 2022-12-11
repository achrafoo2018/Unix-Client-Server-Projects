CC = gcc
CFLAGS = -Wall -g

all: Server Client

Server: Server.c
	$(CC) $(CFLAGS) -o $@ $^

Client: Client.c
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -f Server Client
	rm fifo1 fifo2

