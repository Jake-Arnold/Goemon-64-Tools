#include "m2c_types.h"

s32 func_800347C8_353C8(s32, s32, u16);
void func_80034CB4_358B4(s32);
s32 func_80035A6C_3666C(s32, s16, s32);

s32 func_8003492C_3552C(s32 arg0, s32 arg1, s16 arg2, u16 arg3) {
    s32 temp_v0;

    temp_v0 = func_800347C8_353C8(arg0, arg1, arg3);
    if (temp_v0 == 0) {
        return 0;
    }
    if (temp_v0 != 0) {
        if (func_80035A6C_3666C(temp_v0, arg2, 1) == 0) {
            func_80034CB4_358B4(temp_v0);
            return 0;
        }
    }
    return temp_v0;
}
