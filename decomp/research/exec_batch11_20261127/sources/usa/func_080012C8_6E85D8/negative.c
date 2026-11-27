#include "m2c_types.h"
void func_80218D7C_5D424C(s32, s32, s32, s32);
void func_8021927C_5D474C(s32);
void func_8021B09C_5D656C(s32, s32, s32);

void func_080012C8_6E85D8(s32 arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        ((void (*)(s32, s32, s32, s32))func_80218D7C_5D424C)(arg0, 0, 0, 0);
        ((void (*)(s32))func_8021927C_5D474C)(arg0);
        ((void (*)(s32, s32, s32))func_8021B09C_5D656C)(arg0, 0, 1);
    }

    *(volatile int *)0x80000000 = 1;
}
