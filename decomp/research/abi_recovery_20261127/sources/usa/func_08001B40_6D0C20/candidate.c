#include "m2c_types.h"
s32 func_080016A8_6D0788();                         /* extern */
extern char func_8021927C_5D474C;
extern char func_8021ADD0_5D62A0;
extern char func_8021B09C_5D656C;
extern char func_8021E71C_5D9BEC;

void func_08001B40_6D0C20(void *arg0, void *arg1) {
    if (func_080016A8_6D0788() == 0) {
        ((M2C_UNK (*)(void *, M2C_UNK))&func_8021E71C_5D9BEC)(arg0, 0x3F800000);
        M2C_FIELD(arg1, s16 *, 0x16) = ((s16 (*)(f32, f32))&func_8021ADD0_5D62A0)(M2C_FIELD(arg0, f32 *, 0x78), M2C_FIELD(arg0, f32 *, 0x80));
        ((M2C_UNK (*)(void *))&func_8021927C_5D474C)(arg0);
        ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK))&func_8021B09C_5D656C)(arg0, 0, 0);
    }
}
