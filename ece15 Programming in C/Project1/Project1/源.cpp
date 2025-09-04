#include <stdio.h>
#include <stdlib.h>

void findingfactors(int number)
{
    for (int j = 1; j <= (number / 2); ++j) {
        if ((number % j) == 0) {
            printf("%-5d", j);
        }
    }
    printf("\n");


}



int main()
{
    int num1, num2, i, midnum;

    printf("please enter two integer values\n");
    scanf_s("%d%d", &num1, &num2);
    if (num1 > num2) {
        midnum = num1;
        num1 = num2;
        num2 = midnum;

    }

    printf("%-10s%s\n", "Number", "Factors of this number");

    for (i = num1; i <= num2; ++i) {
        printf("%-10d", i);
        findingfactors(i);

    }







    return 0;
}