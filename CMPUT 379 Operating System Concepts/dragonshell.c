#include <string.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

/**
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Name : Felix Ye
# SID : 1626332
# CCID : hye3
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
*/
/**
 * @brief Tokenize a C string 
 * 
 * @param str - The C string to tokenize 
 * @param delim - The C string containing delimiter character(s) 
 * @param argv - A char* array that will contain the tokenized strings
 * Make sure that you allocate enough space for the array.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <sys/wait.h>

#define MAX_INPUT 1024
#define MAX_TOKENS 100

typedef enum { RUNNING, SUSPENDED } proc_state;

typedef struct process {
    pid_t pid;
    proc_state state;
    char command[MAX_INPUT];
    struct process *next;
} process_t;

process_t *process_table = NULL;
pid_t foreground_pid = 0;

void tokenize(char* str, const char* delim, char ** argv) {
  char* token;
  token = strtok(str, delim);
  for(size_t i = 0; token != NULL; ++i){
    argv[i] = token;
  token = strtok(NULL, delim);
  }
}

void add_process(pid_t pid, proc_state state, const char *cmd) {
    process_t *p = malloc(sizeof(process_t));
    p->pid = pid;
    p->state = state;
    strncpy(p->command, cmd, MAX_INPUT-1);
    p->command[MAX_INPUT-1] = '\0';
    p->next = process_table;
    process_table = p;
}

void remove_process(pid_t pid) {
    process_t **curr = &process_table;
    while (*curr) {
        if ((*curr)->pid == pid) {
            process_t *tmp = *curr;
            *curr = (*curr)->next;
            free(tmp);
            return;
        }
        curr = &((*curr)->next);
    }
}

void suspend_process(pid_t pid) {
    process_t *p = process_table;
    while (p) {
        if (p->pid == pid) {
            p->state = SUSPENDED;
            return;
        }
        p = p->next;
    }
}

void print_jobs() {
    process_t *p = process_table;
    while (p) {
        printf("%d %c %s\n", p->pid, (p->state == RUNNING ? 'R' : 'T'), p->command);
        p = p->next;
    }
}

/**singal*/
void sigint_handler(int sig) {
    if (foreground_pid > 0)
        kill(foreground_pid, SIGINT);
}

void sigtstp_handler(int sig) {
    if (foreground_pid > 0) {
        kill(foreground_pid, SIGTSTP);
        suspend_process(foreground_pid);
        printf("\n");
    }
}

void sigchld_handler(int sig) {
    int status;
    pid_t pid;
    while ((pid = waitpid(-1, &status, WNOHANG | WUNTRACED)) > 0) {
        if (WIFEXITED(status) || WIFSIGNALED(status))
            remove_process(pid);
        else if (WIFSTOPPED(status))
            suspend_process(pid);
    }
}

int handle(char **argv) {
    char *cmd = argv[0];
    char *arg = argv[1];

    if (strcmp(cmd, "pwd") == 0) {
        char cwd[1024];
        if (getcwd(cwd, sizeof(cwd)) != NULL)
            printf("%s\n", cwd);
        else
            perror("getcwd");
        return 1;
    } 
    else if (strcmp(cmd, "cd") == 0) {
        if (!arg)
            fprintf(stderr, "dragonshell: Expected argument to \"cd\"\n");
        else if (chdir(arg) != 0)
            fprintf(stderr, "dragonshell: No such file or directory\n");
        return 1;
    } 
    else if (strcmp(cmd, "jobs") == 0) {
        print_jobs();
        return 1;
    } 
    else if (strcmp(cmd, "exit") == 0) {
        process_t *p = process_table;
        while (p) {
            kill(p->pid, SIGTERM);
            p = p->next;
        }
        while (process_table != NULL) sleep(1);
        exit(0);
    }

    return 0; 
}

int main(int argc, char **argv) {
    char buf[MAX_INPUT];
    char *argv[MAX_TOKENS];

    printf("Welcome to Dragon Shell!\n");

    signal(SIGINT, sigint_handler);
    signal(SIGTSTP, sigtstp_handler);
    signal(SIGCHLD, sigchld_handler);

    while (1) {
        printf("dragonshell> ");
        fflush(stdout);

        if (!fgets(buf, sizeof(buf), stdin)) break;
        buf[strcspn(buf, "\n")] = '\0';
        if (strlen(buf) == 0) continue;

        memset(argv, 0, sizeof(argv));
        tokenize(buf, " \t", argv);
        if (!argv[0]) continue;

        int result = handle(argv);
        if (result == -1) break;

        // external
        int n = 0;
        while (argv[n] != NULL) n++;
        int background = 0;

      
        if (n > 0 && strcmp(argv[n-1], "&") == 0) {
          background = 1;
          argv[n-1] = NULL; 
        }

        pid_t pid = fork();
        if (pid == 0) { // child
            execvp(argv[0], argv);
            perror("dragonshell");
            exit(1);
        } 
        else if (pid > 0) { // father
            if (background) {
              add_process(pid, RUNNING, buf);
              printf("PID %d is sent to background\n", pid); 
            } 
            else {
              foreground_pid = pid;
              int status;
              waitpid(pid, &status, WUNTRACED);
              if (WIFSTOPPED(status)) add_process(pid, SUSPENDED, buf){
                foreground_pid = 0;
              }
                
            }
         }
    }

    return 0;
}