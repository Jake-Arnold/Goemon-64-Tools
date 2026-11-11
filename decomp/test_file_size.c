#include <assert.h>

typedef struct {
    unsigned int start;
    unsigned int end;
} FileExtent;

FileExtent D_80054ACC_556CC[3] = {
    {10, 15},
    {0xFFFFFFFFu, 1},
    {400, 500},
};

unsigned int func_80001DC0_29C0(unsigned int index);

int main(void) {
    assert(func_80001DC0_29C0(0) == 0);
    assert(func_80001DC0_29C0(1) == 5);
    assert(func_80001DC0_29C0(2) == 2);
    assert(func_80001DC0_29C0(3) == 100);
    assert(D_80054ACC_556CC[1].start == 0xFFFFFFFFu);
    return 0;
}
