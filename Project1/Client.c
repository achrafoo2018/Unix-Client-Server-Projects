#include "serv_cli_fifo.h"
#include "Handlers_Cli.h"
int main(){
    /* Déclarations */
    char *pipe_fifo1 = FIFO1;
    char *pipe_fifo2 = FIFO2;
    int fd1, fd2;
    struct reponse resp;
    struct question quest;
    /* Ouverture des tubes nommés */
    fd1 = open(pipe_fifo1, O_WRONLY);
    fd2 = open(pipe_fifo2, O_RDONLY);
    /* Installation des Handlers */
    signal(SIGUSR1, hand_reveil);
    /* Construction et envoi d’une question */
    quest.pid = getpid();
    srand(getpid());
    quest.n = rand() % NMAX + 1;
    write(fd1, &quest, sizeof(quest));
    /* Attente de la réponse */
    pause();
    /* Lecture de la réponse */
    read(fd2, &resp, sizeof(resp));
    /* Envoi du signal SIGUSR1 au serveur */
    kill(resp.pid, SIGUSR1);
    /* Traitement local de la réponse */    
    printf("================================================================\n");
    for(int i=0; i < quest.n; i++){
        printf("%d ", resp.resultat[i]);
    }
    printf("\n===============================================================\n");
    fflush(stdout);
    return 0;    
}
