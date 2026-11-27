#include "m2c_types.h"

extern u8 func_800141C4_14DC4[];
extern u8 func_802171A8_5D2678[];

void *func_08000000_707A40(s32 arg0, s32 arg1, u8 arg2, u16 arg3) {
    void *ret;

    ret = ((void *(*)(s32, s32, u8))func_802171A8_5D2678)(arg0, arg1, arg2);
    if (ret != NULL) {
        M2C_FIELD(ret, u16 *, 0x28) = arg3;
        M2C_FIELD(ret, s32 *, 0x2C) = ((s32 (*)(u16))func_800141C4_14DC4)(arg3);
    }
    { *(volatile int *)0x80000000 = 1; } return ret;
}
