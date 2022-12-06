#include "serv_cli_fifo.h"
#include "Handlers_Serv.h"


int main(){
        /*Déclarations */
        char *pipe_fifo1 = FIFO1;
        char *pipe_fifo2 = FIFO2;
        int fd1, fd2;
        struct reponse resp;
        struct question quest;

        /* Création des tubes nommés */
        mkfifo(pipe_fifo1, 0666);
        mkfifo(pipe_fifo2, 0666);
        /*initialisation du générateur de nombres aléatoires*/
        srand(getpid());
        /* Ouverture des tubes nommés */
        fd1 = open(pipe_fifo1, O_RDWR);
        fd2 = open(pipe_fifo2, O_WRONLY);
        /* Installation des Handlers */
        for(int i=1; i <= NSIG; i++){
                signal(i, fin_serveur);
        }
        signal(SIGUSR1, hand_reveil);
        while(1){
                /* lecture d’une question */
                read(fd1, &quest, sizeof(quest));
                printf("Question recue du processus: %d\n", quest.pid);
                fflush(stdout);
                /* construction de la réponse */
                resp.pid = getpid();
                for(int i=0; i < quest.n; i++){
                        resp.resultat[i] = rand() % NMAX + 1;
                }
                /* envoi de la réponse */
                write(fd2, &resp, sizeof(resp));
                /* envoi du signal SIGUSR1 au client concerné */
                kill(quest.pid, SIGUSR1);
        }
        return 0;
}