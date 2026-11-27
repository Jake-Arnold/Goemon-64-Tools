#include "m2c_types.h"
extern char func_8021927C_5D474C;
extern char func_80219578_5D4A48;
extern char func_8021ADD0_5D62A0;
extern char func_8021B09C_5D656C;

void func_08000EFC_6E4EDC(void *arg0, void *arg1) {
    ((M2C_UNK  (*)(void *, M2C_UNK))&func_80219578_5D4A48)(arg0, 0x3F800000);
    M2C_FIELD(arg1, s16 *, 0x16) = ((s16 (*)(f32, f32))&func_8021ADD0_5D62A0)(M2C_FIELD(arg0, f32 *, 0x78), M2C_FIELD(arg0, f32 *, 0x80));
    ((M2C_UNK (*)(void *))&func_8021927C_5D474C)(arg0);
    ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK))&func_8021B09C_5D656C)(arg0, 1, 0);
}
