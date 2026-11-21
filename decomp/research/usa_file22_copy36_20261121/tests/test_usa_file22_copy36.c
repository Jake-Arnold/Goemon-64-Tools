#include <assert.h>
#include <stdio.h>
#include <stdint.h>
typedef struct { unsigned int word[9]; } Data36;
Data36 D_801D7030_6A9C50;
extern void func_801CBF5C_69EB7C(const Data36 *src);
int main(void) {
    Data36 src;
    for (unsigned repetition=0;repetition<256;repetition++) {
        for (unsigned i=0;i<9;i++) src.word[i]=0xA5D42E19u^(repetition*271u)^(i*49157u);
        func_801CBF5C_69EB7C(&src);
        for (unsigned i=0;i<9;i++) assert(D_801D7030_6A9C50.word[i]==src.word[i]);
    }
    puts("PASS: 256 source-input patterns, 36-byte aggregate copy");
    return 0;
}
