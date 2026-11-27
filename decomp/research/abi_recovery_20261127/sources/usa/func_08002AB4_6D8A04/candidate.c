#include "m2c_types.h"
extern char func_802197D8_5D4CA8;
extern char func_8021ADD0_5D62A0;
extern char func_8021B09C_5D656C;
extern char func_8021C194_5D7664;

void func_08002AB4_6D8A04(void *arg0, void *arg1) {
    M2C_FIELD(arg0, s8 *, 0xDC) = 4;
    ((M2C_UNK  (*)(void *, M2C_UNK))&func_802197D8_5D4CA8)(arg0, 8);
    if (!(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        ((M2C_UNK (*)(void *, M2C_UNK))&func_8021C194_5D7664)(arg0, 0x3F000000);
        M2C_FIELD(arg0, f32 *, 0x7C) = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0x7C) + 3.0);
        M2C_FIELD(arg1, s16 *, 0x16) = ((s16 (*)(f32, f32))&func_8021ADD0_5D62A0)(M2C_FIELD(arg0, f32 *, 0x78), M2C_FIELD(arg0, f32 *, 0x80));
        ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK))&func_8021B09C_5D656C)(arg0, 0, 0);
    }
}
