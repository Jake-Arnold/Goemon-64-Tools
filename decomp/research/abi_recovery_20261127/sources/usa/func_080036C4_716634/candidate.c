#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_80216E1C_5D22EC;
extern char func_8021DEC4_5D9394;
extern M2C_UNK func_08003770_7166E0;

void func_080036C4_716634(void *arg0, void *arg1) {
    M2C_FIELD(arg0, s32 *, 0x60) = 0x20;
    M2C_FIELD(arg0, s16 *, 0x5E) = (s16) M2C_FIELD(arg0, s32 *, 0xD8);
    ((M2C_UNK  (*)(void *, M2C_UNK))&func_80216E1C_5D22EC)(arg0, 0);
    M2C_FIELD(arg1, s8 *, 5) = 5;
    M2C_FIELD(arg1, s32 *, 0x30) = (s32) (((s32 (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK, s32))&func_8021DEC4_5D9394)(arg0, 0xFF, 0, 0, 0) | 0x40000000 | 0x20000000);
    M2C_FIELD(arg1, f32 *, 0x24) = 1.0f;
    M2C_FIELD(arg1, f32 *, 0x20) = 1.0f;
    M2C_FIELD(arg1, f32 *, 0x1C) = 1.0f;
    ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_08003770_7166E0);
}
