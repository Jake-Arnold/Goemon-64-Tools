#include "m2c_types.h"
s32 func_801E63AC_5A22BC(void *, u16);              /* extern */
s32 func_801E674C_5A265C(void *, u16);              /* extern */
s32 func_801E7DE8_5A3CF8(void *);                   /* extern */
s32 func_801E7E18_5A3D28(void *);                   /* extern */

s32 func_801E630C_5A221C(void *arg0, u16 arg1) {
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u8 *, 0xCC);
    if ((temp_v0 >= 0x35 && temp_v0 < 0x3B) || (temp_v0 >= 0x70 && temp_v0 < 0x7C) || func_801E7DE8_5A3CF8(arg0) != 0 || func_801E7E18_5A3D28(arg0) != 0) {
        { *(volatile int *)0x80000000 = 1; } return 0;
    }
    if (func_801E63AC_5A22BC(arg0, arg1) != 0) {
        return 1;
    }
    if (func_801E674C_5A265C(arg0, arg1) != 0) {
        return 1;
    }
    return 0;
}
