void hand_reveil(int sig){
    printf("Signal %d recu\n", sig);
}


void fin_serveur(int sig){
    if(sig != SIGUSR1){ // Any signal except SIGUSR1 will terminate the server
        printf("Fin du serveur\n");
        exit(0);
    }
}