#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80216E1C_5D22EC;
extern char func_8021A310_5D57E0;
extern void *D_801FC60C_5B851C;
extern M2C_UNK func_0800134C_71CDCC;

void func_08001298_71CD18(void *arg0, void *arg1) {
    M2C_FIELD(arg0, s32 *, 0x60) = 0x220;
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x2C4;
    ((M2C_UNK  (*)(void *, M2C_UNK))&func_80216E1C_5D22EC)(arg0, 2);
    M2C_FIELD(arg0, s16 *, 0x8A) = 0x14;
    ((M2C_UNK (*)(void *))&func_8021A310_5D57E0)(arg0);
    M2C_FIELD(arg1, f32 *, 8) = (f32) M2C_FIELD(D_801FC60C_5B851C, f32 *, 8);
    M2C_FIELD(arg1, f32 *, 0xC) = (f32) ((f64) M2C_FIELD(D_801FC60C_5B851C, f32 *, 0xC) + 20.0);
    M2C_FIELD(arg1, f32 *, 0x10) = (f32) M2C_FIELD(D_801FC60C_5B851C, f32 *, 0x10);
    ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_0800134C_71CDCC);
}
