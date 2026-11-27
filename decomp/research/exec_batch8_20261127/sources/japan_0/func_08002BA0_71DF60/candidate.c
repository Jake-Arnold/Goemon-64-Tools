#include "m2c_types.h"
void func_80023CF8_248F8(s32);

void func_08002BA0_71DF60(void) {
    void (*fn)(s32) = func_80023CF8_248F8;

    fn(0x1BD);
    fn(0x1BE);
    fn(0x1BF);
    fn(0x1C0);
}
