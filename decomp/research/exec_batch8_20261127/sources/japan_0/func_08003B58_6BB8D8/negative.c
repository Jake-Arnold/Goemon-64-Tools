#include "m2c_types.h"
extern u8 func_80034E8C_35A8C[];
extern u8 func_80221398_5DC928[];
extern M2C_UNK func_08003BB8_6BB938;

void func_08003B58_6BB8D8(void *arg0, void *arg1) {
    if (!(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        M2C_FIELD(arg1, s16 *, 0x16) = 0;
        ((void (*)(void *, s32))func_80221398_5DC928)(arg0, 0x41200000);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x1E;
        ((void (*)(M2C_UNK *))func_80034E8C_35A8C)(&func_08003BB8_6BB938);
    }

    *(volatile s32 *)0x80000000 = 1;
}
