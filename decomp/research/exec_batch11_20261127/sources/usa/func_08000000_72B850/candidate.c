#include "m2c_types.h"

extern u8 func_800141C4_14DC4[];
extern u8 func_802171A8_5D2678[];

void *func_08000000_72B850(s32 arg0, s32 arg1, u8 arg2) {
    void *temp_v0;

    temp_v0 = ((void *(*)(s32, s32, u8))func_802171A8_5D2678)(arg0, arg1, arg2);
    if (temp_v0 != NULL) {
        M2C_FIELD(temp_v0, s16 *, 0x28) = 0x45;
        M2C_FIELD(temp_v0, s32 *, 0x2C) = ((s32 (*)(s32))func_800141C4_14DC4)(0x45);
    }
    return temp_v0;
}
