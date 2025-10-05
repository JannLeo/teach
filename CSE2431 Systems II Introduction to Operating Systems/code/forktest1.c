#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

int main() {
	pid_t ret_val;  /*statement 1 */
	pid_t pid;	/*statement 2*/
	int i = 0;	/*statement 3*/

	ret_val = fork();       /*statement 4*/
	i = 10;             /*statement 5*/

	if (ret_val < 0) {     /*statement 6*/
		printf("Error on fork. Exiting.\n");    /*statement 7*/
		exit (1);      /*statement 8*/
	}

	else if (ret_val == 0) {    /*statement 9*/
	  printf("pid = %d; i = %d\n\n", getpid(), i); /*statement 10*/
	}

	else {
	  printf("pid = %d; i = %d\n\n", getpid(), i); /*statement 11*/
	}

	return (0);     /*statement 12*/
}
