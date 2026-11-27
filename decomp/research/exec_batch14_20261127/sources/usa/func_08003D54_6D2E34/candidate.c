#include "m2c_types.h"

extern u8 func_8021B988_5D6E58[];
extern u8 func_8021B09C_5D656C[];

void func_08003D54_6D2E34(void *arg0, void *arg1) {
    if (((s32 (*)(void *, f32, f32, f32, f32))func_8021B988_5D6E58)(
            arg0,
            (f32)*(s16 *)((u8 *)arg0 + 0xA0),
            (f32)*(s16 *)((u8 *)arg0 + 0xE0),
            (f32)*(s16 *)((u8 *)arg0 + 0xA2),
            1.0f) == 0) {
        ((void (*)(void *, s32, s32))func_8021B09C_5D656C)(arg0, 1, 1);
    }
}
