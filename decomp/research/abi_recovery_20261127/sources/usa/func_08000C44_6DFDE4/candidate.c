#include "m2c_types.h"
extern char func_8021927C_5D474C;
extern char func_80219448_5D4918;
extern char func_8021ADD0_5D62A0;
extern char func_8021B09C_5D656C;
extern char func_8021BC04_5D70D4;

void func_08000C44_6DFDE4(void *arg0, void *arg1) {
    ((M2C_UNK (*)())&func_80219448_5D4918)();
    ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK))&func_8021BC04_5D70D4)(arg0, 0x3F800000, 0x41800000);
    M2C_FIELD(arg1, s16 *, 0x16) = ((s16 (*)(f32, f32))&func_8021ADD0_5D62A0)(M2C_FIELD(arg0, f32 *, 0x78), M2C_FIELD(arg0, f32 *, 0x80));
    ((M2C_UNK (*)(void *))&func_8021927C_5D474C)(arg0);
    ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK))&func_8021B09C_5D656C)(arg0, 1, 0);
}
