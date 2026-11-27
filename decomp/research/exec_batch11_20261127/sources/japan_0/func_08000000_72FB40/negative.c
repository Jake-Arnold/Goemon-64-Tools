#include "m2c_types.h"

extern u8 func_80013D54_14954[];
extern u8 func_8021BF18_5D74A8[];

void *func_08000000_72FB40(s32 arg0, s32 arg1, u8 arg2) {
    void *temp_v0;

    temp_v0 = ((void *(*)(s32, s32, u8))func_8021BF18_5D74A8)(arg0, arg1, arg2);
    if (temp_v0 != NULL) {
        M2C_FIELD(temp_v0, s16 *, 0x28) = 0x45;
        M2C_FIELD(temp_v0, s32 *, 0x2C) = ((s32 (*)(s32))func_80013D54_14954)(0x45);
    }
    { *(volatile int *)0x80000000 = 1; } return temp_v0;
}
