void hand_reveil(int sig){
    printf("Signal %d received\n", sig);
}


void fin_serveur(int sig){
    if(sig != SIGUSR1){ // Any signal except SIGUSR1 will terminate the server
        printf("Signal %d received, terminating server\n", sig);
        exit(0);
    }
}