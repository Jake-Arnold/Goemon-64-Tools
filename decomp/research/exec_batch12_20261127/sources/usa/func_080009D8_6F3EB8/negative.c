#include "m2c_types.h"

extern u8 func_8003521C_35E1C[];
extern u8 func_8021A26C_5D573C[];
extern u8 func_08000A60_6F3F40[];

void func_080009D8_6F3EB8(void *arg0, void *arg1) {
    M2C_FIELD(arg1, u16 *, 0x16) = (u16) ((M2C_FIELD(arg1, u16 *, 0x16) + 0x40) & 0x3FF);
    M2C_FIELD(arg0, u8 *, 0xD1) = (u8) (M2C_FIELD(arg0, u8 *, 0xD1) - 2);
    ((void (*)(void *, u8, s32, s32, s32))func_8021A26C_5D573C)(arg0, M2C_FIELD(arg0, u8 *, 0xD1), 0, 0, 0);
    if (M2C_FIELD(arg0, u8 *, 0xD1) == 0) {
        ((void (*)(u8 *))func_8003521C_35E1C)(func_08000A60_6F3F40);
        M2C_FIELD(arg0, s16 *, 0x8A) = 5;
        M2C_FIELD(arg0, s32 *, 0x60) = 0;
    }

    *(volatile int *)0x80000000 = 1;
}
