#include "m2c_types.h"
extern u8 func_80034E8C_35A8C[];
extern u8 func_80221398_5DC928[];
extern u8 func_08002EA8_6D69A8[];

void func_08002E44_6D6944(void *arg0, M2C_UNK arg1) {
    if (!(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        ((void (*)(void *, f32))func_80221398_5DC928)(arg0, 4.0f / 3.0f);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x14;
        ((void (*)(void *))func_80034E8C_35A8C)(func_08002EA8_6D69A8);
    }
}
