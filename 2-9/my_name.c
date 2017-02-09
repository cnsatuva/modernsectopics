#include <stdio.h>

int main() {
	char buf[12];
  	printf("Your name: ");
  	gets(buf);
  	printf("Hello, %s\n", buf);
	return 0;
}
