#include "m2c_types.h"

extern u8 func_80034E8C_35A8C[];
extern u8 func_8021E46C_5D99FC[];
extern u8 func_080010EC_6DB98C[];

void func_08001070_6DB910(void *arg0, s32 arg1) {
    *(f32 *)((u8 *)arg0 + 0x80) = 0.0f;
    *(f32 *)((u8 *)arg0 + 0x78) = 0.0f;
    if (((s32 (*)(void *, f32, f32, f32, s32))func_8021E46C_5D99FC)(
            arg0, (f32)*(s16 *)((u8 *)arg0 + 0xA0), 0.0f, (f32)*(s16 *)((u8 *)arg0 + 0xA2), 8) == 0) {
        ((void (*)(void *))func_80034E8C_35A8C)(func_080010EC_6DB98C);
    }
}
