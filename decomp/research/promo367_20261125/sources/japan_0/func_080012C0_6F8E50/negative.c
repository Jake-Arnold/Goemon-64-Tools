#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
extern M2C_UNK D_80162420_163020;
extern M2C_UNK func_08002250_6F9DE0;

void func_080012C0_6F8E50(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_v0;

    M2C_FIELD(&D_80162420_163020, s32 *, 0xD4) = (s32) (M2C_FIELD(&D_80162420_163020, s32 *, 0xD4) | 1);
    temp_v0 = M2C_FIELD(arg0, u8 *, 0xD0);
    if (temp_v0 == 0) {
        ((M2C_UNK(*)())&func_80038808_39408)(0x224);
    } else if (temp_v0 == 1) {
        ((M2C_UNK(*)())&func_80038808_39408)(0x224);
    } else if (temp_v0 == 2) {
        ((M2C_UNK(*)())&func_80038808_39408)(0x224);
    } else if (temp_v0 == 3) {
        ((M2C_UNK(*)())&func_80038808_39408)(0x227);
    } else if (temp_v0 == 4) {
        ((M2C_UNK(*)())&func_80038808_39408)(0x15F);
    } else if (temp_v0 == 6) {
        ((M2C_UNK(*)())&func_80038808_39408)(0x224);
    } else if (temp_v0 == 7) {
        ((M2C_UNK(*)())&func_80038808_39408)(0x15D);
    } else if (temp_v0 == 8) {
        ((M2C_UNK(*)())&func_80038808_39408)(0x15F);
    } else {
        ((M2C_UNK(*)())&func_80038808_39408)(0x15E);
    }
    M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 1);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_08002250_6F9DE0);
}
