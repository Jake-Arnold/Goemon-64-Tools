#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
M2C_UNK func_0800166C_6C0DBC();                     /* static */
extern f32 D_080089C4_6C8114;

void func_08001600_6C0D50(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & 0xFEFFFFFF);
        M2C_FIELD(arg0, f32 *, 0x7C) = (f32) D_080089C4_6C8114;
        ((M2C_UNK(*)())&func_80038B98_39798)(0x154);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_0800166C_6C0DBC);
    }
}
