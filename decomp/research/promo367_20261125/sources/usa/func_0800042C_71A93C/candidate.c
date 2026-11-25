#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80221FB0_5DD480;
extern M2C_UNK D_8015CC30_15D830;
extern void *D_801FC604_5B8514;
extern M2C_UNK func_080004B4_71A9C4;

void func_0800042C_71A93C(void *arg0, s8 *arg1) {
    s8 *temp_v0;

    temp_v0 = M2C_FIELD(arg0, s8 **, 0xD0);
    if (M2C_FIELD(D_801FC604_5B8514, u16 *, 0x98) == 0) {
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x84), f32 *, 8) = (f32) M2C_FIELD(&D_8015CC30_15D830, f32 *, 0x194);
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x84), f32 *, 0x10) = (f32) M2C_FIELD(&D_8015CC30_15D830, f32 *, 0x198);
        return;
    }
    arg1 = temp_v0;
    ((M2C_UNK(*)())&func_80221FB0_5DD480)();
    *arg1 = 8;
    ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_080004B4_71A9C4);
}
