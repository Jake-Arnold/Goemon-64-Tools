#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);
extern M2C_UNK func_08007BB4_6BF934;

void func_08007B4C_6BF8CC(void *arg0, void *arg1) {
    M2C_FIELD(arg1, u16 *, 0x16) = (M2C_FIELD(arg1, u16 *, 0x16) + 4) & 0x3FF;
    M2C_FIELD(arg0, s32 *, 0xE8) &= ~0x3000;
    M2C_FIELD(arg0, s32 *, 0xE8) |= 0x2000;
    if (M2C_FIELD(arg1, u16 *, 0x16) == 0x360) {
        M2C_UNK (*fn)(M2C_UNK *) = func_80034E8C_35A8C;
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x3C;
        fn(&func_08007BB4_6BF934);
    }

    *(volatile s32 *)0x80000000 = 1;
}
