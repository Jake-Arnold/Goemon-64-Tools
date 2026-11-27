#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);
extern M2C_UNK func_08001B44_6F96D4;

void func_08001538_6F90C8(void *arg0, void *arg1) {
    M2C_UNK (*fn)(M2C_UNK *) = func_80034E8C_35A8C;
    void *temp_v0 = M2C_FIELD(arg0, void **, 0xDC);
    void *temp_v1 = M2C_FIELD(temp_v0, void **, 0x18);

    M2C_FIELD(arg1, u16 *, 0x16) = M2C_FIELD(temp_v1, u16 *, 0x16);
    M2C_FIELD(temp_v0, s32 *, 0xEC) &= ~4;
    if (M2C_FIELD(arg0, u16 *, 0xDA) != 0) {
        M2C_FIELD(temp_v0, s32 *, 0xEC) |= 4;
        M2C_FIELD(arg0, u16 *, 0xDA) = 0;
    }
    if (M2C_FIELD(temp_v0, s32 *, 0xEC) & 1) {
        fn(&func_08001B44_6F96D4);
    }

    *(volatile s32 *)0x80000000 = 1;
}
