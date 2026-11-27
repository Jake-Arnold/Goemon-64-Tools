#include "m2c_types.h"

extern u8 func_8021B988_5D6E58[];
extern u8 func_8003521C_35E1C[];
extern u8 func_08003148_6FE348[];
void func_080028B4_6FDAB4(void *);

void func_08003074_6FE274(void *arg0, void *arg1) {
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x9C);
    if (temp_v0 != NULL) {
        M2C_FIELD(temp_v0, f32 *, 0xD0) = M2C_FIELD(arg1, f32 *, 8);
        M2C_FIELD(temp_v0, f32 *, 0xD4) = M2C_FIELD(arg1, f32 *, 0xC);
        M2C_FIELD(temp_v0, f32 *, 0xD8) = M2C_FIELD(arg1, f32 *, 0x10);
    }
    if (((s32 (*)(void *, f32, f32, f32, f32))func_8021B988_5D6E58)(
            arg0,
            (f32)M2C_FIELD(arg0, s16 *, 0xC8),
            (f32)M2C_FIELD(arg0, s16 *, 0xCA),
            (f32)M2C_FIELD(arg0, s16 *, 0xCC),
            (f32)((f32)M2C_FIELD(arg0, s16 *, 0xD6) / 20.0)) == 0) {
        ((void (*)(void *))func_8003521C_35E1C)(func_08003148_6FE348);
    }
    M2C_FIELD(arg0, s16 *, 0xEC) = 0;
    func_080028B4_6FDAB4(arg0);

    *(volatile int *)0x80000000 = 1;
}
