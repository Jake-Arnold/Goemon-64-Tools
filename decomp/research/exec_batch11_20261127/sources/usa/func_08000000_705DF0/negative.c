#include "m2c_types.h"

extern u8 func_800141C4_14DC4[];
extern u8 func_802171A8_5D2678[];

void *func_08000000_705DF0(s32 arg0, s32 arg1, u8 arg2) {
    void *ret;

    ret = ((void *(*)(s32, s32, u8))func_802171A8_5D2678)(arg0, arg1, arg2);
    if (ret != NULL) {
        M2C_FIELD(ret, s16 *, 0x28) = 0x2F;
        M2C_FIELD(ret, s32 *, 0x2C) = ((s32 (*)(s32))func_800141C4_14DC4)(0x2F);
    }
    { *(volatile int *)0x80000000 = 1; } return ret;
}
