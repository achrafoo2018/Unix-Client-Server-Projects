// C program for the Server Side
#include "Server_Client.h"

void *client_thread(void *arg)
{
	printf("Client thread created\n");
    // Get the client socket from the argument
    int client_sockfd = *((int *) arg);

	int client_request;
    // Read the random number n sent by the client
	read(client_sockfd, &client_request, sizeof(client_request));

    // Generate an array of n random numbers
    int random_numbers[client_request];
    for (int i = 0; i < client_request; i++)
    {
        random_numbers[i] = rand() % NMAX + 1;
    }
    // Send the array of random numbers to the client
	write(client_sockfd, random_numbers, sizeof(random_numbers));

    // Close the connection
    close(client_sockfd);

    return NULL;
}

// Driver Code
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

	// Listen on the socket, with 100 max connection requests queued
	if (listen(serverSocket, 100) == 0)
		printf("Server listening on port %d...\n", PORT);
	else
		printf("Error\n");


	while (1) {
		addr_size = sizeof(serverStorage);

		// Extract the first connection in the queue
		client_sockfd = accept(serverSocket, 
								(struct sockaddr*)&serverStorage,
								&addr_size);

		pthread_t thread_id;
        if (pthread_create(&thread_id, NULL, client_thread, &client_sockfd))
        {
            perror("pthread_create");
            return EXIT_FAILURE;
        }

	}

	return 0;
}
