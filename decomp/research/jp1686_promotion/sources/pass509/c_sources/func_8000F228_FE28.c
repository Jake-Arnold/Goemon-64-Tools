#include "m2c_types.h"
M2C_UNK func_8000F1E0_FDE0(u16, s32, void *, s32);  /* extern */
f32 func_8001C7C8_1D3C8(s32, s32, s32, s32, f32 *, f32 *); /* extern */

void func_8000F228_FE28(u16 arg0, s32 arg1, void *arg2, s32 arg3) {
    f32 sp24;
    f32 sp20;

    if ((func_8001C7C8_1D3C8(arg1, M2C_FIELD(arg2, s32 *, 8), M2C_FIELD(arg2, s32 *, 0xC), M2C_FIELD(arg2, s32 *, 0x10), &sp24, &sp20) >= 0.0f) && !(sp24 < 0.0f) && !(sp24 > 320.0f) && !(sp20 < 0.0f) && !(sp20 > 240.0f)) {
        func_8000F1E0_FDE0(arg0, arg1, arg2, arg3);
    }
}
