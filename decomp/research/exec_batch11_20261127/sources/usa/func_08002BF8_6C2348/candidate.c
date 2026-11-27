#include "m2c_types.h"
extern u8 func_80023DF0_249F0[];
extern u8 func_8003521C_35E1C[];
extern f64 D_08008A00_6C8150;
extern u8 func_08002C68_6C23B8[];

void func_08002BF8_6C2348(void *arg0, void *arg1) {
    M2C_FIELD(arg1, f32 *, 0xC) = (f32) ((f64) M2C_FIELD(arg1, f32 *, 0xC) - D_08008A00_6C8150);
    ((void (*)(s32))func_80023DF0_249F0)(1);
    if (M2C_FIELD(arg0, u16 *, 0x8A)--) {
    } else {
        ((void (*)(void *))func_8003521C_35E1C)(func_08002C68_6C23B8);
    }
}
