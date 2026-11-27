#include "m2c_types.h"
extern u8 func_8003521C_35E1C[];
extern u8 func_8021C628_5D7AF8[];
extern M2C_UNK func_08003C1C_6B6EBC;

void func_08003BBC_6B6E5C(void *arg0, void *arg1) {
    if (!(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        M2C_FIELD(arg1, s16 *, 0x16) = 0;
        ((void (*)(void *, s32))func_8021C628_5D7AF8)(arg0, 0x41200000);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x1E;
        ((void (*)(M2C_UNK *))func_8003521C_35E1C)(&func_08003C1C_6B6EBC);
    }

    *(volatile s32 *)0x80000000 = 1;
}
