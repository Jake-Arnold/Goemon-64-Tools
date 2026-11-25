#include "m2c_types.h"
extern char func_80034B44_35744;
extern char func_80034E8C_35A8C;
extern char func_8021F080_5DA610;
extern char func_8021FDBC_5DB34C;
extern M2C_UNK func_08001BEC_71908C;

void func_08001B58_718FF8(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if ((s32) temp_v0 <= 0) {
        ((M2C_UNK(*)())&func_80034B44_35744)();
        return;
    }
    if (!(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        ((M2C_UNK(*)())&func_8021F080_5DA610)();
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 0x20);
        ((M2C_UNK(*)())&func_8021FDBC_5DB34C)(arg0);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_08001BEC_71908C);
    }
}
