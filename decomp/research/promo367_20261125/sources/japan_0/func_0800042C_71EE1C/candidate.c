#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_80226D20_5E22B0;
extern M2C_UNK D_80162420_163020;
extern void *D_80201514_5BD4E4;
extern M2C_UNK func_080004B4_71EEA4;

void func_0800042C_71EE1C(void *arg0, s8 *arg1) {
    s8 *temp_v0;

    temp_v0 = M2C_FIELD(arg0, s8 **, 0xD0);
    if (M2C_FIELD(D_80201514_5BD4E4, u16 *, 0x98) == 0) {
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x84), f32 *, 8) = (f32) M2C_FIELD(&D_80162420_163020, f32 *, 0x194);
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x84), f32 *, 0x10) = (f32) M2C_FIELD(&D_80162420_163020, f32 *, 0x198);
        return;
    }
    arg1 = temp_v0;
    ((M2C_UNK(*)())&func_80226D20_5E22B0)();
    *arg1 = 8;
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_080004B4_71EEA4);
}
