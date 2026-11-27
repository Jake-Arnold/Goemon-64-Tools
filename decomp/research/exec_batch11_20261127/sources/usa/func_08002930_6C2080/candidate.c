#include "m2c_types.h"
extern u8 func_80023DF0_249F0[];
extern u8 func_8003521C_35E1C[];
extern f64 D_080089E8_6C8138;
extern u8 func_080029A0_6C20F0[];

void func_08002930_6C2080(void *arg0, void *arg1) {
    M2C_FIELD(arg1, f32 *, 0xC) = (f32) ((f64) M2C_FIELD(arg1, f32 *, 0xC) - D_080089E8_6C8138);
    ((void (*)(s32))func_80023DF0_249F0)(0);
    if (M2C_FIELD(arg0, u16 *, 0x8A)--) {
    } else {
        ((void (*)(void *))func_8003521C_35E1C)(func_080029A0_6C20F0);
    }
}
