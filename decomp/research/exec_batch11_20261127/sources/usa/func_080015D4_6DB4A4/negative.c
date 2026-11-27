#include "m2c_types.h"
void func_8003521C_35E1C(void *);
s32 func_802196FC_5D4BCC(void *, s32, s32, s32, s32);
extern M2C_UNK func_0800162C_6DB4FC;

void func_080015D4_6DB4A4(void *arg0, void *arg1) {
    if (((s32 (*)(void *, s32, s32, s32, s32))func_802196FC_5D4BCC)(arg0, M2C_FIELD(arg0, s32 *, 0xDC), M2C_FIELD(arg1, s32 *, 0xC), M2C_FIELD(arg0, s32 *, 0xE0), 0x20) == 0) {
        ((void (*)(void *))func_8003521C_35E1C)(&func_0800162C_6DB4FC);
    }

    *(volatile int *)0x80000000 = 1;
}
