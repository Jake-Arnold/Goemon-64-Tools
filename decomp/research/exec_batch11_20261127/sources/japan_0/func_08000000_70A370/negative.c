#include "m2c_types.h"

extern u8 func_80013D54_14954[];
extern u8 func_8021BF18_5D74A8[];

void *func_08000000_70A370(s32 arg0, s32 arg1, u8 arg2) {
    void *ret;

    ret = ((void *(*)(s32, s32, u8))func_8021BF18_5D74A8)(arg0, arg1, arg2);
    if (ret != NULL) {
        M2C_FIELD(ret, s16 *, 0x28) = 0x2F;
        M2C_FIELD(ret, s32 *, 0x2C) = ((s32 (*)(s32))func_80013D54_14954)(0x2F);
    }
    { *(volatile int *)0x80000000 = 1; } return ret;
}
