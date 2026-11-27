#include "m2c_types.h"
void func_80034E8C_35A8C(void *);
void func_8021B3BC_5D694C(s32, s32, f32, s32);
extern u8 func_08000AC4_71BE84[];

void func_08000A74_71BE34(s32 arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        ((void (*)(s32, s32, f32, s32))func_8021B3BC_5D694C)(arg0, 0, 0.25f, 1);
        ((void (*)(void *))func_80034E8C_35A8C)(func_08000AC4_71BE84);
    }
}
