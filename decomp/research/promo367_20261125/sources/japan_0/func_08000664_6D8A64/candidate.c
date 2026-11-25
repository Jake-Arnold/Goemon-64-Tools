#include "m2c_types.h"
extern char func_8000F1E0_FDE0;
extern char func_80034E8C_35A8C;
extern char func_8021B3BC_5D694C;
extern M2C_UNK D_802119E0_5CD9B0;
extern M2C_UNK func_08000720_6D8B20;

void func_08000664_6D8A64(void *arg0, void *arg1) {
    u16 temp_v0;

    temp_v0 = M2C_FIELD(arg1, u16 *, 0x14);
    if (temp_v0 != 0x300) {
        M2C_FIELD(arg1, u16 *, 0x14) = (u16) ((temp_v0 - 0x20) & 0x3FF);
    } else {
        M2C_FIELD(arg0, s8 *, 0x9B) = (s8) -M2C_FIELD(arg0, u8 *, 0x9A);
    }
    if (!(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        ((M2C_UNK(*)())&func_8000F1E0_FDE0)(0x262, &D_802119E0_5CD9B0, arg1, 0x43C80000);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x1E;
        M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
        ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 3, 0x3E800000, 1);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_08000720_6D8B20);
    }
}
