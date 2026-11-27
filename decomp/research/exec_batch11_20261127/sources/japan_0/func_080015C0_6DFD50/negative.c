#include "m2c_types.h"
void func_80034E8C_35A8C(void *);
s32 func_8021E46C_5D99FC(void *, s32, s32, s32, s32);
extern M2C_UNK func_08001618_6DFDA8;

void func_080015C0_6DFD50(void *arg0, void *arg1) {
    if (((s32 (*)(void *, s32, s32, s32, s32))func_8021E46C_5D99FC)(arg0, M2C_FIELD(arg0, s32 *, 0xDC), M2C_FIELD(arg1, s32 *, 0xC), M2C_FIELD(arg0, s32 *, 0xE0), 0x20) == 0) {
        ((void (*)(void *))func_80034E8C_35A8C)(&func_08001618_6DFDA8);
    }

    *(volatile int *)0x80000000 = 1;
}
