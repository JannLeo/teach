#include <stdio.h>   
#include <stdlib.h>  
#include <unistd.h> 
#include <sys/wait.h> 
#include <string.h>   
#include <errno.h>
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



#define MAX_INPUT 1024
#define MAX_TOKEN 100

typedef enum { RUNNING, SUSPENDED } proc_state;

typedef struct process {
    pid_t pid;
    proc_state state;
    char command[MAX_INPUT];
    struct process *next;
} process_t;

process_t *process_table = NULL;
pid_t external_pid = 0;

//seperate token, command and input
void tokenize(char* str, const char* delim, char ** argv) {
  char* token;
  token = strtok(str, delim);
  for(size_t i = 0; token != NULL; ++i){
    argv[i] = token;
  token = strtok(NULL, delim);
  }
}

// add new process
void add_process(pid_t pid, proc_state state, const char *cmd) {
    process_t *p = malloc(sizeof(process_t));
    p->pid = pid;
    p->state = state;
    strncpy(p->command, cmd, MAX_INPUT-1);
    p->command[MAX_INPUT-1] = '\0';
    p->next = process_table;
    process_table = p;
}

// cltra + C and free malloc space
void remove_process(pid_t pid) {
    process_t **current = &process_table;
    while (*current) {
        if ((*current)->pid == pid) {
            process_t *tmp = *current;
            *current = (*current)->next;
            free(tmp);
            return;
        }
        current = &((*current)->next);
    }
}

// cltra + Z
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
    if (external_pid > 0)
        kill(external_pid, SIGINT);
}

// cltra +z
void sigtstp_handler(int sig) {
    if (external_pid > 0) {
        kill(external_pid, SIGTSTP);
        suspend_process(external_pid);
        printf("\n");
    }
}

// cltra + C or cltra Z
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
    char *word = argv[0];
    char *arg = argv[1];

    if (strcmp(word, "pwd") == 0) {
        char cwd[1024];
        if (getcwd(cwd, sizeof(cwd)) != NULL)
            printf("%s\n", cwd);
        else
            perror("getcwd");
        return 1;
    } 

    else if (strcmp(word, "cd") == 0) {
        if (!arg)
            fprintf(stderr, "dragonshell: Expected argument to \"cd\"\n");
        else if (chdir(arg) != 0)
            fprintf(stderr, "dragonshell: No such file or directory\n");
        return 1;
    } 

    else if (strcmp(word, "jobs") == 0) {
        print_jobs();
        return 1;
    } 

    else if (strcmp(word, "exit") == 0) {
        process_t *p = process_table;
        while (p) {
            kill(p->pid, SIGTERM);
            p = p->next;
        }
        // 通过 sigchld 清理
        while (waitpid(-1, NULL, 0) > 0) {
        }
        return -1;
    }

    return 0; 
}

void double_quotes(char *s) {
    int len = strlen(s);
    if (len >= 2 && 
       ((s[0] == '"' && s[len-1] == '"') || 
        (s[0] == '\'' && s[len-1] == '\''))) {
        s[len-1] = '\0';  
        memmove(s, s+1, len-1); 
    }
}

int main(int argc, char **argv) {
    char buf[MAX_INPUT];
    char *arg[MAX_TOKEN];

    printf("Welcome to Dragon Shell!\n");

    signal(SIGINT, sigint_handler);
    signal(SIGTSTP, sigtstp_handler);
    signal(SIGCHLD, sigchld_handler);

    while (1) {
        printf("dragonshell> ");
        fflush(stdout);

        if (!fgets(buf, sizeof(buf), stdin)){
            break;
        }
        buf[strcspn(buf, "\n")] = '\0';
        if (strlen(buf) == 0) {
            continue;
        }
        
        
        memset(arg, 0, sizeof(arg));
        tokenize(buf, " \t", arg);
        if (!arg[0]) {
            continue;
        }

        int result = handle(arg);
        if (result == -1) {
            break; // exit
        }
        else if (result == 1){
            continue; //not external command
        }

        // external
        int n = 0;
        while (arg[n] != NULL) n++;
        int test = 0;
        
        char *input = NULL;
        char *output = NULL;
        char *filename = NULL;

        for (int i = 0; i < n; i++) {
            if (strcmp(arg[i], "<") == 0 && i+1 < n) {
                input = arg[i+1];
                double_quotes(arg[i-1]);
                arg[i] = NULL; 
                arg[i+1] = NULL;
                i++;
            }
            if (strcmp(arg[i], ">") == 0 && i+1 < n) {
                output = arg[i+1];
                double_quotes(arg[i-1]);
                arg[i] = NULL; 
                arg[i+1] = NULL;
                i++;
            }
            if (strcmp(arg[i], "|") == 0 && i+1 < n) {
                test = 2;
            }
        }

        if (n > 0 && strcmp(arg[n-1], "&") == 0) {
          test = 1;
          arg[n-1] = NULL; 
        }

        if (test == 2) {
            int fd[2];
            pipe(fd);
            pid_t pid1 = fork();
            if (pid1 == 0) { // cmd1
                dup2(fd[1], STDOUT_FILENO);
                close(fd[0]);
                close(fd[1]);
                execvp(cmd1_argv[0], cmd1_argv);
                exit(1);
            }

            pid_t pid2 = fork();
            if (pid2 == 0) { // cmd2
                dup2(fd[0], STDIN_FILENO);
                close(fd[1]);
                close(fd[0]);
                execvp(cmd2_argv[0], cmd2_argv);
                exit(1);
            }

            close(fd[0]);
            close(fd[1]);
            waitpid(pid1, NULL, 0);
            waitpid(pid2, NULL, 0);
            continue;
            
        }
        

        pid_t pid = fork();
        if (pid == 0) { // child
            if (input) {
                int file = open(input, O_RDONLY);
                if (file < 0) {
                    perror("open infile");
                    exit(1);
                }
                dup2(file, STDIN_FILENO);
                close(file);
            }
    
            if (output) {
                int file = open(output, O_WRONLY | O_CREAT | O_TRUNC, 0644);
                if (file < 0) {
                    perror("open outfile");
                    exit(1);
                }
                dup2(file, STDOUT_FILENO);
                close(file);
            }

            execvp(arg[0], arg);
            exit(1);
        } 
        else if (pid > 0) { // father
            if (test) {
              add_process(pid, RUNNING, buf);
              printf("PID %d is sent to background\n", pid); 
            } 
            else {
                external_pid = pid;
                int status;
                waitpid(pid, &status, WUNTRACED); 
                external_pid = 0;    
                
            }
         }
    }

    return 0;
}