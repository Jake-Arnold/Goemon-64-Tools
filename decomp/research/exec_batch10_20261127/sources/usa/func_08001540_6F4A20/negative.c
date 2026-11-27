#include "m2c_types.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);
extern M2C_UNK func_08001B4C_6F502C;

void func_08001540_6F4A20(void *arg0, void *arg1) {
    M2C_UNK (*fn)(M2C_UNK *) = func_8003521C_35E1C;
    void *temp_v0 = M2C_FIELD(arg0, void **, 0xDC);
    void *temp_v1 = M2C_FIELD(temp_v0, void **, 0x18);

    M2C_FIELD(arg1, u16 *, 0x16) = M2C_FIELD(temp_v1, u16 *, 0x16);
    M2C_FIELD(temp_v0, s32 *, 0xEC) &= ~4;
    if (M2C_FIELD(arg0, u16 *, 0xDA) != 0) {
        M2C_FIELD(temp_v0, s32 *, 0xEC) |= 4;
        M2C_FIELD(arg0, u16 *, 0xDA) = 0;
    }
    if (M2C_FIELD(temp_v0, s32 *, 0xEC) & 1) {
        fn(&func_08001B4C_6F502C);
    }

    *(volatile s32 *)0x80000000 = 1;
}
