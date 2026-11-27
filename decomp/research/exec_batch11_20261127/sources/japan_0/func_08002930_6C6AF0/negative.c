#include "m2c_types.h"
extern u8 func_80023AB0_246B0[];
extern u8 func_80034E8C_35A8C[];
extern f64 D_080089E8_6CCBA8;
extern u8 func_080029A0_6C6B60[];

void func_08002930_6C6AF0(void *arg0, void *arg1) {
    M2C_FIELD(arg1, f32 *, 0xC) = (f32) ((f64) M2C_FIELD(arg1, f32 *, 0xC) - D_080089E8_6CCBA8);
    ((void (*)(s32))func_80023AB0_246B0)(0);
    if (M2C_FIELD(arg0, u16 *, 0x8A)--) {
    } else {
        ((void (*)(void *))func_80034E8C_35A8C)(func_080029A0_6C6B60);
    }

    *(volatile int *)0x80000000 = 1;
}
