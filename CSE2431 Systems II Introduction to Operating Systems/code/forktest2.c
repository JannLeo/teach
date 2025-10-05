#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

void functionA(int *value);  	/* functionA declaration */
void functionB(int value);	/* functionB declaration */

int main()
{

	pid_t ret_val;
	pid_t pid;
	int num = 20;

	ret_val = fork();

	if (ret_val < 0) {
		printf ("Error on fork. Exiting.\n");
		exit (1);
	}
	else if (ret_val == 0) {
		functionA(&num);
		printf("\nI called functionA, I have pid %i: num = %i\n\n", getpid(), num);
		printf("\n***Process which called functionA is done ***\n\n");
	}
	else {
		functionB(num);
		printf("\nI called functionB, I have pid %i: num = %i\n\n", getpid(), num); 
		printf("\n***Process which called functionB is done***\n\n");
	}
	return (0);
}

void functionB(int value)
{
  value += 0;
}

void functionA(int *value)
{	
  *value += 25;
}
