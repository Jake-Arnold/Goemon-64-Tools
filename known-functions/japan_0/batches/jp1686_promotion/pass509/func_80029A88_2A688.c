#include "m2c_types.h"
s32 func_80029DE8_2A9E8(f32, f32, s32);             /* extern */
s32 func_800322EC_32EEC(f32, f32);                  /* extern */

s32 func_80029A88_2A688(f32 arg0, f32 arg1, s32 arg2) {
    if (func_800322EC_32EEC(arg0, arg1) == 0x7FFF) {
        return 0x7FFF;
    }
    return func_80029DE8_2A9E8(arg0, arg1, arg2);
}
