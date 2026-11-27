#include "m2c_types.h"
M2C_UNK func_801ED918_5A98E8(void *, u16); /* extern */

void func_801ED8E0_5A98B0(void *arg0, u16 arg1, s32 arg2) {
    M2C_FIELD(arg0, s32 *, 0x80) = arg2;
    M2C_FIELD(arg0, s8 *, 0x86) = 0;
    M2C_FIELD(arg0, s16 *, 0x84) = -1;
    func_801ED918_5A98E8(arg0, arg1);
}
