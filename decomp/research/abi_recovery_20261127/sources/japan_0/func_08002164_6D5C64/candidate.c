#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021B3BC_5D694C;
extern char func_8021E548_5D9AD8;
extern M2C_UNK func_080021E8_6D5CE8;

void func_08002164_6D5C64(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
    if (((s32  (*)(void *, M2C_UNK))&func_8021E548_5D9AD8)(arg0, 0x10) == 0) {
        ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_8021B3BC_5D694C)(arg0, 1, 0x3EAAAAAB, 0);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x12;
        ((M2C_UNK (*)(M2C_UNK *))&func_80034E8C_35A8C)(&func_080021E8_6D5CE8);
    }
}
