//---------------------------------------------------
//#include <stdio.h>
//char* process(char x[]) {
//	printf("%d \n", sizeof(x));
//	return x + 2;
//}
//int main() {
//	char a[5] = "cat";
//	char* p = a;
//	p = process(a);
//	printf("%c \n", p[-2]);
//	p = a + 1;
//	printf("%c \n", p[0]);
//	printf("%c \n", ++(*a));
//}

//------------------------------------------------------
//#include <stdio.h>
//int main() {
//	int a = 2.5;
//	printf("%d -> %c \n", a, a + 'a');
//	a = 9;
//	double b = a / (char)2.5;
//	printf("%1.2f \n", b);
//	if ('=')
//		printf("dog \n");
//	else
//		printf("cat \n");
//	a = (8 > 0 && 1 < 2) ? (1 == 0) : (0 == 0);
//	printf("%d \n", a);
//}
//------------------------------------------------------

//#include <stdio.h>
//#define VALUE 4
//int dec(int x, int y) {
//	int value = 1;
//	x = VALUE;
//	printf(" %d \n", x);
//	return 2 + y;
//	return 3 + y;
//}
//double inc(double* x, double* y) {
//	*x += 1;
//	*y -= 2;
//	return *x + 1;
//}
//int main() {
//	int x = 2, y = 6;
//	y = dec(x, y);
//	printf(" %d %d\n", x, y);
//	double a = 1, b = 8;
//	b = inc(&a, &b);
//	printf(" %1.2f %1.2f\n", a, b);
//}
//------------------------------------------------------
//#include <stdio.h>
//#include <stdlib.h>
//void process(int* x) {
//	printf("%d \n", x[0] + 2 * x[1]);
//	x += 1;
//	x[0] += 5;
//}
//int main() {
//	int n;
//	scanf_s("%d", &n);
//	int a[3] = { 0 };
//	int* p = (int*)calloc(n, sizeof(int));
//	//int* p = (int*)malloc(n*sizeof(int));
//	printf("%d \n", sizeof(a));
//	printf("%d \n", sizeof(p));
//	process(p);
//	printf("%d \n", p[0] + 2 * p[1]);
//	free(p);
//}
//------------------------------------------------------
//#include <stdio.h>
//typedef enum { mo = 4, tu, we, th = 9, fi } days;
//int main() {
//	int a[2][3] = { 3, 5, 7, 9, 11, 13 };
//	days b = we;
//	printf("%d \n", a[1][1]);
//	printf("%d %d \n", b, b + 1);
//}
//------------------------------------------------------
//#include <stdio.h>
//int process(int a) {
//	a = 1;
//	static int c = 3;
//	c++;
//	return c;
//}
//int main() {
//	int x = 1;
//	while (x < 10) {
//		x += 3;
//		if (x % 2 == 0)
//			continue;
//		printf("%d ", x);
//	}
//	printf("\n");
//	int a = 4, b = 3;
//	if (b > 0) {
//		int a = 0;
//		b = process(3);
//		printf("%d %d \n", a, b);
//		a = 7;
//		b = process(a);
//		printf("%d %d \n", a, b);
//	}
//	printf("%d \n", a);
//}
//------------------------------------------------------
// 
// 
// 
// 
// 
// 
//#include <stdio.h>
//int process(int *a, int b) {
//	(*a)++;
//	return -b;
//}
//int main() {
//	int a = 9, b = 5, result;
//	// Call your function process() (single line of code)
//	result = process(&a, b);
//	printf("%d %d %d ", a, b, result);
//}
// ------------------------------------------------------
// 10
//bool two_digits(int num) {
//	if (num >= 10 && num <= 99) {
//		return true;
//	}
//	return false;
//}
//void swap(int *swap_num) {
//	int a = (*swap_num) % 10;
//	int b = (*swap_num) / 10;
//	(*swap_num) = 10 * a + b;
//}
//
//void swapif(int* num) {
//
//	if (two_digits(*num)) {
//		swap(num);
//	}
//}
//
//void process(int *a , int count) {
//	for (int i = 0; i < count; i++) {
//		swapif(&(a[i]));
//		//swapif(a + i);
//	}
//}
//
//#include <stdio.h>
//int main() {
//	int vals[] = { 6, 92, 123, 34 };
//	int num = 78;
//	int count = sizeof(vals) / sizeof(vals[0]);
//	if (two_digits(num)) {
//		// Call your function swap() (single line of code)
//		swap(&num);
//	}	
//	// Call your function process() on vals (single line of code)
//	process(vals, count);
//	printf("num: %d \n", num);
//	printf("vals: %d %d %d %d", vals[0], vals[1], vals[2], vals[3]);
//}
// 
// ---------------------------------------------------
//#include <stdio.h>
//int count(char symbol, char text[]) {
//	int count = 0;
//	for (int i = 0; text[i] != '\0'; i++) {
//		if (*(text + i) == symbol) {
//			count++;
//		}
//	}
//	return count;
//}
//
//void alpha(char text[], char letters[]) {
//	int i = 0;
//	int c = 0;
//	for (i = 0; text[i] != '\0'; i++) {
//		char a = 'a' + c;
//		letters[i] = a;
//		c++;
//		if (c == 26) {
//			c = 0;
//		}
//	}
//	letters[i] = '\0';
//
//}
//
//int main() {
//	char text[] = "It is a very pretty cat! Yes, it is.";
//	char symbol = 'e';
//	int num;
//	// Declare the variable letters; this variable will store the
//	char letters[101];
//	// output string of the function alpha() (single line of code)
//	alpha(text, letters);
//	// Call your function count() (single line of code)
//	num = count(symbol, text);
//	// Call your function alpha() (single line of code)
//	printf("The letters string: %s \n", letters);
//	printf("The symbol occurs %d times", num);
//}
// ---------------------------------------------------
//#include <stdio.h>
//#include <stdlib.h>
//#include <time.h>
//typedef struct {
//	int value; // The result of the dice roll
//} Dice;
//void roll(Dice *d) {
//	d->value = rand() % 6 + 1;
//}
//int main() {
//	int i;
//	Dice d;
//	// Any other line(s) of code you may need (optional)
//	srand(time(NULL));
//	for (i = 0; i < 10; i++) {
//		// Any other line(s) of code you may need (optional)
//		
//		// Call your function roll() (single line of code)
//		roll(&d);
//		printf("%d ", d.value);
//	}
//}
// ---------------------------------------------------
//#include <karel.h>
//// Helper functions would go here
//static int count() {
//	return ++;
//}
//int main() {
//	karel_setup("settings/settings.json");
//	// Your main code would go here
//	while (!wall_in_front()) {
//
//	}
//}
// -----------------------------------------------
//#include <stdio.h>
//int* process(int* x) {
//	*x = *x + 1;
//	x = x + 2;
//	return x;
//}
//int main() {
//	int* p;
//	int a = 5;
//	p = process(&a);
//	printf("%d \n", a);
//	printf("%d \n", *p);
//	int b[4] = { 7, 5, 3 };
//	p = process(b + 1);
//	printf("%d \n", p[0]);
//	printf("%d \n", b[1]);
//}
//------------------------------------------------------
//#include <stdio.h>
//void process(char z[]) {
//	*(z + 1) = '\0';
//	printf("%d \n", sizeof(z));
//}
//int main() {
//	char x[] = { 'a','b','c'};
//	char y[] = "def";
//	printf("%d \n", sizeof(x) + 1);
//	printf("%d \n", sizeof(y) + 1);
//	printf("%d \n", sizeof(x + 1));
//	printf("%s", x);
//	process(x + 1);
//	printf("%s \n", x);
//}
////------------------------------------------------------
//#include <stdio.h>
//int main() {
//	char x = 1.5;
//	double y = 'd', z = 1.5;
//	int k = 2;
//	x += (int)2.75;
//	printf("%1.2f \n", x + 0.5);
//	printf("%c \n", (char)(y + 3 * z));
//	printf("%1.2f\n", (double)((int)3 * z));
//	printf("%d \n", k > -2);
//	printf("%d \n", '\0' ? --k : ++k);
//}
//------------------------------------------------------
//#include <stdio.h>
//int a;
//int process(int a) {
//	a = a + a;
//	return a;
//}
//int calc() {
//	static int x = 3;
//	x = a + x;
//	return x;
//}
//int main() {
//	printf("%d \n", a);
//	a = 0;
//	printf("%d \n", process(++a));
//	a = 1;
//	if (1) {
//		int a = 5;
//		printf("%d \n", a + calc());
//		printf("%d \n", process(++a));
//		a = 2;
//	}
//	printf("%d \n", a + calc());
//}
//------------------------------------------------------
// 
//#include <stdio.h>
//#define DIM 6
//void swap1(int* a, int* b) {
//	int i = 0;
//	while (a[i] >= 0) {
//		i++;
//	}
//	int temp = a[i];
//	a[i] = *b;
//	*(b) = temp;
//}
//int swap2(int a[], int b) {
//	int i = 0;
//	while (a[i] >= 0) {
//		i++;
//	}
//	int temp = a[i];
//	a[i] = b;
//	return temp;
//}
//int main() {
//	int a[DIM] = { 2,6,3,-1,2,9 };
//	int i, b = -5;
//	// Call your swap1() function (single line of code)
//	swap1(a, &b);
//	printf("%d \t", b);
//	for (i = 0; i < DIM; i++)
//		printf("%d ", a[i]);
//	// Call your swap2() function (single line of code)
//	b = swap2(a, b);
//	printf("\n%d \t", b);
//	for (i = 0; i < DIM; i++)
//		printf("%d ", a[i]);
//}
// -----------------------------------------------
//#include <stdio.h>
//#include <stdlib.h>
//typedef struct {
//	int number; // The house number
//	char street[50]; // The street name
//} Address;
//typedef struct {
//	int pid; // The PID of the student
//	char name[50]; // The name of the student
//	int* grades; // Dynamic array with student’s grades
//	Address address; // The address of the student
//} Student;
//void print_name(Student stu) {
//	printf("%s\n", stu.name);
//}
//void set_pid(Student* stu,int pid) {
//	stu->pid = pid;
//}
//void init_grades(Student* stu, int n) {
//	stu->grades = (int*)malloc(n*sizeof(int));
//	for (int i = 0; i < n; i++) {
//		stu->grades[i] = 0;
//	}
//}
//void set_grade(Student stu,int index ,int grade) {
//	stu.grades[index] = grade;
//}
//char get_street_letter(Student stu) {
//	return stu.address.street[0];
//}
//int main() {
//	Student student1 = { 0, "Jane Doe", NULL, {9500,"Gilman"} };
//	// The function print_name() prints the name of the student
//	print_name(student1);
//	// The function set_pid() sets the pid of the student to
//	// the value that is passed as the second argument
//	int pid = 1234567;
//	set_pid(&student1, pid);
//	// The function init_grades() creates a new dynamic array that
//	// is linked to by the grades field in the student struct. The
//	// size of the dynamic array is given by the second argument.
//	// All elements of the dynamic array should be initialized to 0.
//	int num_grades = 4;
//	init_grades(&student1, num_grades);
//	// The function set_grade() sets the grade at a specific index
//	// in the dynamic array to the value given as the third argument.
//	int index = 1, value = 12;
//	set_grade(student1, index, value);
//	// The function get_street_letter() returns the first letter of
//	// the street that is listed in the address of the student.
//	char c = get_street_letter(student1);
//}
// -----------------------------------------------
//#include <stdio.h>
//#include <stdlib.h>
//char* next(char* sentence,int reset) {
//	int i = 0;
//	static char* word;
//	if (reset == 1) {
//		word = sentence;
//		return word;
//	}
//	
//	while (word[i] != ' ' && word[i] != '\0') {
//		i++;
//	}
//	if (word[i] == '\0') {
//		return NULL;
//	}
//	word += (i + 1);
//	
//	return word;
//}
//void modify(char* sentence) {
//	sentence[0] = '0'+(sentence[0] - 'a' + 1) % 10;
//}
//void cut(char *a,char *b) {
//	//递归
//	if (*a == '\0' || *b == '\0') {
//		*a = '0';
//		return;
//	}
//	cut(a + 1, b + 1);
//}
//int abc() {
//	return abc() + 1;
//}
//int main() {
//	char sentence[] = "go to the beach";
//	char word[] = "overlord";
//	char* p;
//	int reset = 1;
//	do {
//		p = next(sentence, reset);
//		reset = 0;
//		if (p != NULL)
//			printf("Next: %s \n", p);
//	} while (p != NULL);
//	modify(sentence);
//	printf("Modify: %s \n", sentence);
//	cut(sentence, word);
//	printf("Cut: %s \n", sentence);
}
// ---------------------------------------------
//#include <stdio.h>
//int main() {
//	int i, j, a;
//	for (i = 0; i < 2; i++) {
//		j = 0;
//		a = 1;
//		while (j < 3) {
//			j += 1;
//			if (j == i) continue;
//			if (j == 2) break;
//			a *= 2;
//		}
//		printf("%d:%d \t", i, a);
//	}
//}
//------------------------------------------------------

#include <stdio.h>

long transfrom(long p, long q, long r) {
	long result = p - (q + r);
	result = result ^ ((q + r) >> 63);
	return result;
}

int main() {
	
}


