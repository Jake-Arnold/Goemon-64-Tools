#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021BB8C_5D711C;
extern char func_80222C34_5DE1C4;
extern M2C_UNK func_0800375C_71ABFC;

void func_080036B0_71AB50(void *arg0, void *arg1) {
    M2C_FIELD(arg0, s32 *, 0x60) = 0x20;
    M2C_FIELD(arg0, s16 *, 0x5E) = (s16) M2C_FIELD(arg0, s32 *, 0xD8);
    ((M2C_UNK  (*)(void *, M2C_UNK))&func_8021BB8C_5D711C)(arg0, 0);
    M2C_FIELD(arg1, s8 *, 5) = 5;
    M2C_FIELD(arg1, s32 *, 0x30) = (s32) (((s32 (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK, s32))&func_80222C34_5DE1C4)(arg0, 0xFF, 0, 0, 0) | 0x40000000 | 0x20000000);
    M2C_FIELD(arg1, f32 *, 0x24) = 1.0f;
    M2C_FIELD(arg1, f32 *, 0x20) = 1.0f;
    M2C_FIELD(arg1, f32 *, 0x1C) = 1.0f;
    ((M2C_UNK (*)(M2C_UNK *))&func_80034E8C_35A8C)(&func_0800375C_71ABFC);

    *(volatile s32 *)0x80000000 = 1;
}
