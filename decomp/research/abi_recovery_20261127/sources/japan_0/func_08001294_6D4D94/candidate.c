#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021B3BC_5D694C;
extern char func_8021E548_5D9AD8;
extern M2C_UNK func_08001314_6D4E14;

void func_08001294_6D4D94(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
    if (((s32  (*)(void *, M2C_UNK))&func_8021E548_5D9AD8)(arg0, 8) == 0) {
        ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_8021B3BC_5D694C)(arg0, 1, 0x3E800000, 1);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x27;
        ((M2C_UNK (*)(M2C_UNK *))&func_80034E8C_35A8C)(&func_08001314_6D4E14);
    }
}
