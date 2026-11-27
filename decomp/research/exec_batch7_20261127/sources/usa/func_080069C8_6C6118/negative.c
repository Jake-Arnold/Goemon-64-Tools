#include "m2c_types.h"
void func_8003521C_35E1C(void *); /* extern */
extern M2C_UNK func_08006A38_6C6188;

void func_080069C8_6C6118(void *arg0, void *arg1) {
    M2C_FIELD(arg0, f32 *, 0x80) = -4.0f;
    if (M2C_FIELD(arg1, f32 *, 0x10) == -404.0f) {
        M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
        ((void (*)(void *))func_8003521C_35E1C)(&func_08006A38_6C6188);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x3C;
    }

    *(volatile s32 *)0x80000000 = 1;
}
