#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

// rewrite this function to be constant-time
void do_spooky_stuff(char *data) {
    for(int x = 0; x < 9; x++) {
        if (data[x] % 2 == 0) {
            data[x] = data[x] / 2;
        } else {
            if (data[x] % 3 == 0) {
                data[x] = data[x] / 3;
            } else {
                data[x] = data[x] + 1;
            }
        }
    }
}

int main() {
    char data[10] = {0};
    printf("Enter some value\n");
    read(0, data, 9);
    data[9] = 0;
    do_spooky_stuff(data);
    printf("Result: |%s|\n", data);
    return 0;
}
