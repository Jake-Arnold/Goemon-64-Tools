#include "m2c_types.h"
s32 func_8021E024_5D95B4(s32);                      /* extern */

s32 func_8022706C_5E25FC(f32 arg0) {
    s32 var_v1;

    if (func_8021E024_5D95B4(0x64 - (s32) (arg0 * 100.0f)) == 0) {
        var_v1 = 1;
    } else {
        var_v1 = 0;
    }
    return var_v1;
}
