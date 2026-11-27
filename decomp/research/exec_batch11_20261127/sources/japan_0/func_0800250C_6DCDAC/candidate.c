#include "m2c_types.h"
extern u8 func_80034E8C_35A8C[];
extern u8 func_8021E46C_5D99FC[];
extern u8 func_0800257C_6DCE1C[];

void func_0800250C_6DCDAC(void *arg0, M2C_UNK arg1) {
    if (((s32 (*)(void *, f32, f32, f32, s32))func_8021E46C_5D99FC)(arg0, (f32) M2C_FIELD(arg0, s16 *, 0xA0), 0.0f, (f32) M2C_FIELD(arg0, s16 *, 0xA2), 8) == 0) {
        ((void (*)(void *))func_80034E8C_35A8C)(func_0800257C_6DCE1C);
    }
}
