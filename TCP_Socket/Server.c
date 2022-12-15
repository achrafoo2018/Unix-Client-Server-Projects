#include "Server_Client.h"

int main()
{
	// Seed the random number generator with the current time
	srand(time(NULL));
	// Initialize variables
	int serverSocket, client_sockfd;
	struct sockaddr_in serverAddr;
	struct sockaddr_storage serverStorage;
	socklen_t addr_size;

	serverSocket = socket(AF_INET, SOCK_STREAM, 0);
	serverAddr.sin_addr.s_addr = INADDR_ANY;
	serverAddr.sin_family = AF_INET;
	serverAddr.sin_port = htons(PORT);
			
	// Bind the socket to the address and port number.
	bind(serverSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr));

	// open file in previous directory named server.log
	FILE *fp = fopen("../server.log", "w");
	// Listen on the socket, with 100 max connection requests queued
	if (listen(serverSocket, 100) == 0){
		printf("Server listening on port %d...\n", PORT);
		fprintf(fp, "Server listening on port %d...\n", PORT);
	}else{
		printf("Error\n");
		fprintf(fp, "Error\n");
	}
	fflush(stdout);
	fflush(fp);
	while (1) {
		addr_size = sizeof(serverStorage);

		// Extract the first connection in the queue
		client_sockfd = accept(serverSocket, 
								(struct sockaddr*)&serverStorage,
								&addr_size);

		char client_ip[INET_ADDRSTRLEN];
		inet_ntop(AF_INET, &(((struct sockaddr_in *)&serverStorage)->sin_addr), client_ip, INET_ADDRSTRLEN);
		printf("Client connected from %s\n", client_ip);
		fprintf(fp, "Client connected from %s\n", client_ip);
		fflush(stdout);
		fflush(fp);
		if(fork() == 0){
			fflush(stdout);
			int client_request;
			// receive the random number n sent by the client
			recv(client_sockfd, &client_request, sizeof(client_request), 0);

			// Generate an array of n random numbers
			int random_numbers[client_request];
			for (int i = 0; i < client_request; i++){
				random_numbers[i] = rand() % NMAX + 1;
			}

			// Send the array of random numbers to the client
			send(client_sockfd, random_numbers, sizeof(random_numbers), 0);

			// Close the connection
			close(client_sockfd);
			exit(0);
		}else{
			close(client_sockfd);
		}
	}
	return 0;
}
