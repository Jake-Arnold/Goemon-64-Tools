#include "m2c_types.h"
extern char func_80034ED4_35AD4;
extern char func_8003521C_35E1C;
extern char func_8021A310_5D57E0;
extern char func_8021B04C_5D651C;
extern M2C_UNK func_08001BEC_714B5C;

void func_08001B58_714AC8(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if ((s32) temp_v0 <= 0) {
        ((M2C_UNK(*)())&func_80034ED4_35AD4)();
        return;
    }
    if (!(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        ((M2C_UNK(*)())&func_8021A310_5D57E0)();
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 0x20);
        ((M2C_UNK(*)())&func_8021B04C_5D651C)(arg0);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08001BEC_714B5C);
    }
}
