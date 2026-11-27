#include "m2c_types.h"
extern u8 func_80029A88_2A688[];
extern u8 func_80034E8C_35A8C[];
extern u8 func_0800107C_6D9D2C[];

void func_08001318_6D9FC8(void *arg0, void *arg1) {
    if (((s32 (*)(f32, f32, s32))func_80029A88_2A688)(M2C_FIELD(arg1, f32 *, 8), M2C_FIELD(arg1, f32 *, 0xC) - 30.0f, M2C_FIELD(arg1, s32 *, 0x10)) == 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = 0x02A00FE1;
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x96;
        ((void (*)(void *))func_80034E8C_35A8C)(func_0800107C_6D9D2C);
    }
}
