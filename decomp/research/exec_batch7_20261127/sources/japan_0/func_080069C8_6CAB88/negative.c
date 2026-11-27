#include "m2c_types.h"
void func_80034E8C_35A8C(void *); /* extern */
extern M2C_UNK func_08006A38_6CABF8;

void func_080069C8_6CAB88(void *arg0, void *arg1) {
    M2C_FIELD(arg0, f32 *, 0x80) = -4.0f;
    if (M2C_FIELD(arg1, f32 *, 0x10) == -404.0f) {
        M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
        ((void (*)(void *))func_80034E8C_35A8C)(&func_08006A38_6CABF8);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x3C;
    }

    *(volatile s32 *)0x80000000 = 1;
}
