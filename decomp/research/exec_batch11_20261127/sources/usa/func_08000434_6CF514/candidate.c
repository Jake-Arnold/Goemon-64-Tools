#include "m2c_types.h"
void func_802197D8_5D4CA8(s32, s32);
void func_8021B09C_5D656C(s32, s32, s32);
void func_8021BC04_5D70D4(s32, f32, f32);

void func_08000434_6CF514(s32 arg0, M2C_UNK arg1) {
    void (*fn1)(s32, f32, f32) = func_8021BC04_5D70D4;
    void (*fn2)(s32, s32) = func_802197D8_5D4CA8;
    void (*fn3)(s32, s32, s32) = func_8021B09C_5D656C;
    fn1(arg0, 1.0f, 64.0f);
    fn2(arg0, 8);
    fn3(arg0, 1, 0);
}
