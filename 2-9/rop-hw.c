#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

char exec[10];

void call_me_first() {
    strcpy(exec, "/bin");
    strcat(exec, "/bash");
}

void call_me_second() {
    system(exec);
}

int main() {
    char buf[20];
    printf("Your name: ");
    read(0, buf, 40);
    printf("Hello, %s\n", buf);
    return 0;
}
