#include "m2c_types.h"

s32 func_80034B58_35758(s32, s32, u16);
void func_80035044_35C44(s32);
s32 func_80035DFC_369FC(s32, s16, s32);

s32 func_80034CBC_358BC(s32 arg0, s32 arg1, s16 arg2, u16 arg3) {
    s32 temp_v0;

    temp_v0 = func_80034B58_35758(arg0, arg1, arg3);
    if (temp_v0 == 0) {
        { *(volatile int *)0x80000000 = 1; } return 0;
    }
    if (temp_v0 != 0) {
        if (func_80035DFC_369FC(temp_v0, arg2, 1) == 0) {
            func_80035044_35C44(temp_v0);
            return 0;
        }
    }
    return temp_v0;
}
