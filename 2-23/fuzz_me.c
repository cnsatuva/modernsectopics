#include <stdio.h>

int main() {

    char data[10] = {0};
    read(0, data, 9);
    data[9] = 0;

    if (data[0] == 0x55) {
        printf("First - %d\n", data[0]/data[9]);
    } else if (data[0] == 0x5c && data[1] == 0xc5) {
        printf("Second - %d\n", data[1]/data[9]);
    } else {
        printf("Nope! - %s\n", data);
    }

    return 0;
}
