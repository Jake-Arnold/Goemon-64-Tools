#include "m2c_types.h"
void func_80024088_24C88(s32);

void func_08002C30_719AD0(void) {
    void (*fn)(s32) = func_80024088_24C88;

    fn(0x1BD);
    fn(0x1BE);
    fn(0x1BF);
    fn(0x1C0);
}
