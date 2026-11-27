#include "m2c_types.h"

extern u8 func_8021B09C_5D656C[];
extern u8 func_8021BB04_5D6FD4[];

void func_08002C20_6DCAF0(void *arg0, M2C_UNK arg1) {
    if (((s32 (*)(void *, f32, f32, s32))func_8021BB04_5D6FD4)(arg0, (f32) M2C_FIELD(arg0, s16 *, 0xA0), (f32) M2C_FIELD(arg0, s16 *, 0xA2), 0x40000000) == 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = M2C_FIELD(arg0, s32 *, 0x60) & 0xFEFFFFFF;
        ((void (*)(void *, s32, s32))func_8021B09C_5D656C)(arg0, 0, 1);
    }
}
