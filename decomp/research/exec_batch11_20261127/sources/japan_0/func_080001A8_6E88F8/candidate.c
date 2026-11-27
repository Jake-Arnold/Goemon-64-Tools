#include "m2c_types.h"
void func_80034E8C_35A8C(void *);
void func_8021B3BC_5D694C(void *, s32, f32, s32);
extern M2C_UNK func_08000208_6E8958;

void func_080001A8_6E88F8(void *arg0, M2C_UNK arg1) {
    ((void (*)(void *, s32, f32, s32))func_8021B3BC_5D694C)(arg0, 0, 1.0f / 3.0f, 1);
    M2C_FIELD(arg0, s32 *, 0x60) = 0x2016E1;
    ((void (*)(void *))func_80034E8C_35A8C)(&func_08000208_6E8958);
}
