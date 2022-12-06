// C program for the Client Side

#include "Server_Client.h"


// Driver Code
int main()
{
	// Seed the random number generator with the current time
	srand(time(NULL));
	int client_request;
	int network_socket;
	// Create a stream socket
	network_socket = socket(AF_INET,
							SOCK_STREAM, 0);

	// Initialise port number and address
	struct sockaddr_in server_address;
	server_address.sin_family = AF_INET;
	server_address.sin_addr.s_addr = INADDR_ANY;
	server_address.sin_port = htons(PORT);

	// Initiate a socket connection
	int connection_status = connect(network_socket,
									(struct sockaddr*)&server_address,
									sizeof(server_address));

	// Check for connection error
	if (connection_status < 0) {
		perror("Error\n");
		exit(1);
	}

	printf("Connection established\n");

	// Generate a random number client_request
	client_request = rand() % NMAX + 1;
	


    // Send the random number client_request to the server
	write(network_socket, &client_request, sizeof(client_request));
	printf("Sent %ld bytes: %d\n", sizeof(client_request), client_request);
    // Read the array of random numbers sent by the server
    int response[NMAX];
    read(network_socket, response, sizeof(response));
	/* Traitement local de la réponse */    
    printf("================================================================\n");
    for(int i=0; i < client_request; i++){
        printf("%d ", response[i]);
    }
    printf("\n===============================================================\n");
    fflush(stdout);

    // Close the connection
    close(network_socket);

    return 0;
}


