#include "m2c_types.h"
M2C_UNK func_801EA30C_5A62DC();                     /* static */
extern void *D_8020152C_5BD4FC;
extern M2C_UNK g_system;

void func_801EA460_5A6430(void *arg0) {
    void *temp_v0;

    M2C_FIELD(D_8020152C_5BD4FC, s8 *, 0x64) = 1;
    temp_v0 = M2C_FIELD(arg0, void **, 0x5C);
    M2C_FIELD(temp_v0, u16 *, 0x30) = (u16) (M2C_FIELD(temp_v0, u16 *, 0x30) + 1);
    if ((s32) M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), u16 *, 0x30) >= 0x3C) {
        func_801EA30C_5A62DC();
        M2C_FIELD(&g_system, s8 *, 0xCF88D) = 1;
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s16 *, 0x86) = 0;
    }
}
