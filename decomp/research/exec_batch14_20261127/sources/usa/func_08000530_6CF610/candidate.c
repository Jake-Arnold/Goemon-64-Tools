#include "m2c_types.h"

extern u8 func_8021B09C_5D656C[];
extern u8 func_8021B988_5D6E58[];

void func_08000530_6CF610(void *arg0, M2C_UNK arg1) {
    if (((s32 (*)(void *, f32, f32, f32, f32))func_8021B988_5D6E58)(arg0, (f32)M2C_FIELD(arg0, s16 *, 0xA0), (f32)M2C_FIELD(arg0, s16 *, 0xE0), (f32)M2C_FIELD(arg0, s16 *, 0xA2), 1.0f) == 0) {
        ((void (*)(void *, s32, s32))func_8021B09C_5D656C)(arg0, 1, 1);
    }
}
