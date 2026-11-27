#include "m2c_types.h"
s32 func_801EB5DC_5A75AC(void *, u16);              /* extern */
s32 func_801EB8D0_5A78A0(void *, u16);              /* extern */
s32 func_801ECF10_5A8EE0(void *);                   /* extern */
s32 func_801ECF40_5A8F10(void *);                   /* extern */

s32 func_801EB53C_5A750C(void *arg0, u16 arg1) {
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u8 *, 0xCC);
    if ((temp_v0 >= 0x35 && temp_v0 < 0x3B) || (temp_v0 >= 0x70 && temp_v0 < 0x7C) || func_801ECF10_5A8EE0(arg0) != 0 || func_801ECF40_5A8F10(arg0) != 0) {
        return 0;
    }
    if (func_801EB5DC_5A75AC(arg0, arg1) != 0) {
        return 1;
    }
    if (func_801EB8D0_5A78A0(arg0, arg1) != 0) {
        return 1;
    }
    return 0;
}
