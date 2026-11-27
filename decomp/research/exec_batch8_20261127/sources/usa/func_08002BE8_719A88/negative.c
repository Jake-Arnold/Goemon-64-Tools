#include "m2c_types.h"
void func_80024038_24C38(s32);

void func_08002BE8_719A88(void) {
    void (*fn)(s32) = func_80024038_24C38;

    fn(0x1BD);
    fn(0x1BE);
    fn(0x1BF);
    fn(0x1C0);

    *(volatile s32 *)0x80000000 = 1;
}
