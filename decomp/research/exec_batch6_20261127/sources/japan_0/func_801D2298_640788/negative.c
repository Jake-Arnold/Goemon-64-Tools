#include "m2c_types.h"
void *func_800354C4_360C4(M2C_UNK *, M2C_UNK, M2C_UNK, f32, f32, f32, s32, s32, s32, f32, f32, f32, s32, s32); /* extern */
extern M2C_UNK func_801EDB40_65C030;

void func_801D2298_640788(s32 arg0) {
    M2C_FIELD(func_800354C4_360C4(&func_801EDB40_65C030, 0, 0, 0.0f, 0.0f, 0.0f, 0, 0, 0, 0.0f, 0.0f, 0.0f, 0, 0), s32 *, 0xEC) = arg0;

    *(volatile s32 *)0x80000000 = 1;
}
