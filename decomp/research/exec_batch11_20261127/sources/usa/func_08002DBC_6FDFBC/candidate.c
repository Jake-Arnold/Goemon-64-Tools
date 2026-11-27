#include "m2c_types.h"
extern u8 func_80218D7C_5D424C[];

void func_08002DBC_6FDFBC(void *arg0, void *arg1) {
    M2C_FIELD(arg0, s32 *, 0x60) = 0x600080;
    ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))func_80218D7C_5D424C)(arg0, 0x1E, 4, -2);
    M2C_FIELD(arg1, f32 *, 8) = M2C_FIELD(arg0, f32 *, 0xD0);
    M2C_FIELD(arg1, f32 *, 0xC) = M2C_FIELD(arg0, f32 *, 0xD4);
    M2C_FIELD(arg1, f32 *, 0x10) = M2C_FIELD(arg0, f32 *, 0xD8);
    M2C_FIELD(arg0, s32 *, 0xDC) = M2C_FIELD(arg0, s32 *, 0x38);
}
