#include "m2c_types.h"
extern u8 func_80023AB0_246B0[];
extern u8 func_80034E8C_35A8C[];
extern f64 D_08008A00_6CCBC0;
extern u8 func_08002C68_6C6E28[];

void func_08002BF8_6C6DB8(void *arg0, void *arg1) {
    M2C_FIELD(arg1, f32 *, 0xC) = (f32) ((f64) M2C_FIELD(arg1, f32 *, 0xC) - D_08008A00_6CCBC0);
    ((void (*)(s32))func_80023AB0_246B0)(1);
    if (M2C_FIELD(arg0, u16 *, 0x8A)--) {
    } else {
        ((void (*)(void *))func_80034E8C_35A8C)(func_08002C68_6C6E28);
    }
}
