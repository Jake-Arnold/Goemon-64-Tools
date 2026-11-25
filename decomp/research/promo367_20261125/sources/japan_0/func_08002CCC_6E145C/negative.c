#include "m2c_types.h"
extern char func_8000F1E0_FDE0;
extern char func_80034E8C_35A8C;
extern M2C_UNK D_802119E0_5CD9B0;
extern M2C_UNK func_08002D74_6E1504;

void func_08002CCC_6E145C(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    u16 temp_v0;

    temp_v0 = M2C_FIELD(arg1, u16 *, 0x14);
    if (temp_v0 != 0x300) {
        M2C_FIELD(arg1, u16 *, 0x14) = (u16) ((temp_v0 - 0x20) & 0x3FF);
    } else {
        M2C_FIELD(arg0, s8 *, 0x9B) = (s8) -M2C_FIELD(arg0, u8 *, 0x9A);
    }
    if (!(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        ((M2C_UNK(*)())&func_8000F1E0_FDE0)(0x262, &D_802119E0_5CD9B0, arg1, 0x43C80000);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x32;
        M2C_FIELD(arg1, s8 *, 0x7C) = 1;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_08002D74_6E1504);
    }
}
