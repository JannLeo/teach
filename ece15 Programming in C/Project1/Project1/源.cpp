#include <stdio.h>

int main() {
	int start, end;
	char a = 'a';
	char b = '0';
	float flo = 1.2;
	double dou = 3.4;
	char c[10] = {"abcdef"};

	scanf_s("%d",&start);
	scanf_s("%d", &end);
	for (int i = start; i <= end; i++) {
		printf("%10d",i);
	}
	return 0;
}