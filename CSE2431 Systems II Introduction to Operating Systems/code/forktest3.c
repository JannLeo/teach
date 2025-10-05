#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

void Code1(void);  	/* Code1 function declaration */
void Code2(void);	/* Code2 function declaration */

int main()
{
	pid_t ret_val0;

	ret_val0 = fork();

	if (ret_val0 < 0) {
		printf("\nError in fork\n");
		exit(1);
	}
	else if (ret_val0 == 0) {
		Code1();
		Code1();
	}
	else if (ret_val0 > 0) {
		Code2();
		Code2();
	}
	return (0);
}

void Code1() {	
	pid_t ret_val1;
	ret_val1 = fork();
	if (ret_val1 < 0) {
		printf("\nError in fork\n");
		exit(1);
	}
	else if (ret_val1 == 0) {
		pid_t pid = getpid();
		printf("\n\t***This line is from Code1 process, pid = %d***\n", pid);
	}
	else {
		pid_t pid = getpid();
		printf("\n\t***This line is from Code1 process, pid = %d***\n", pid);
	}
}

void Code2() {	
	pid_t ret_val2;
	ret_val2 = fork();
	if (ret_val2 < 0) {
		printf("\nError in fork\n");
		exit(1);
	}
	else if (ret_val2 == 0) {
		pid_t pid = getpid();
		printf("\n\t***This line is from Code2 process, pid = %d***\n", pid);
	}
	else {
		pid_t pid = getpid();
		printf("\n\t***This line is from Code2 process, pid = %d***\n", pid);
	}
}

