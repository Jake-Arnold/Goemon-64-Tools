#include "m2c_types.h"

extern u8 func_800141C4_14DC4[];
extern u8 func_802171A8_5D2678[];

void *func_08000000_70A040(s32 arg0, s32 arg1, u8 arg2, u16 arg3) {
    void *temp_v0;

    temp_v0 = ((void *(*)(s32, s32, u8))func_802171A8_5D2678)(arg0, arg1, arg2);
    if (temp_v0 != NULL) {
        M2C_FIELD(temp_v0, u16 *, 0x28) = arg3;
        M2C_FIELD(temp_v0, s32 *, 0x2C) = ((s32 (*)(u16))func_800141C4_14DC4)(arg3);
    }
    { *(volatile int *)0x80000000 = 1; } return temp_v0;
}
