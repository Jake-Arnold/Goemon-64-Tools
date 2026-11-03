#include "common.h"

s32 func_8002A168_2AD68(f32, f32, f32);
s32 func_8003266C_3326C(f32, f32);

s32 func_80029E08_2AA08(f32 arg0, f32 arg1, f32 arg2) {
    if (func_8003266C_3326C(arg0, arg1) == 0x7FFF) {
        return 0x7FFF;
    }
    return func_8002A168_2AD68(arg0, arg1, arg2);
}
