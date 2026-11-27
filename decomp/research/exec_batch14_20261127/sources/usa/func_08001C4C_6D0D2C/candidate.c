#include "m2c_types.h"

s32 func_080016A8_6D0788(void);
extern u8 func_8021927C_5D474C[];
extern u8 func_80219448_5D4918[];
extern u8 func_8021ADD0_5D62A0[];
extern u8 func_8021B09C_5D656C[];

void func_08001C4C_6D0D2C(void *arg0, void *arg1) {
    if (func_080016A8_6D0788() == 0) {
        ((void (*)(void *))func_80219448_5D4918)(arg0);
        M2C_FIELD(arg1, s16 *, 0x16) = ((s16 (*)(f32, f32))func_8021ADD0_5D62A0)(M2C_FIELD(arg0, f32 *, 0x78), M2C_FIELD(arg0, f32 *, 0x80));
        ((void (*)(void *))func_8021927C_5D474C)(arg0);
        ((void (*)(void *, s32, s32))func_8021B09C_5D656C)(arg0, 0, 0);
    }
}
