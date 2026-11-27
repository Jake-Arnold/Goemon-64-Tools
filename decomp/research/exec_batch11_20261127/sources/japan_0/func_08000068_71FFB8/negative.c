#include "m2c_types.h"
extern u8 func_80034E8C_35A8C[];
extern u8 func_8022B5B0_5E6B40[];
extern M2C_UNK func_080000C0_720010;

void func_08000068_71FFB8(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x2C2;
    ((M2C_UNK (*)(void *, u16))func_8022B5B0_5E6B40)(arg0, M2C_FIELD(arg0, u16 *, 0xD2));
    M2C_FIELD(arg0, s32 *, 0x60) = 0x221;
    ((M2C_UNK (*)(M2C_UNK *))func_80034E8C_35A8C)(&func_080000C0_720010);

    *(volatile int *)0x80000000 = 1;
}
