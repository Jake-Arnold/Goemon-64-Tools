#include "m2c_types.h"
f32 func_801D8660_6030E0(s32, M2C_UNK);             /* extern */
u8 func_801DC2AC_606D2C(M2C_UNK, M2C_UNK);                   /* extern */
M2C_UNK func_801EB0CC_615B4C(s32);                  /* static */
M2C_UNK func_801F4584_61F004(s32);                  /* static */
M2C_UNK func_801F45D0_61F050(s32);                  /* static */

void func_801EB468_615EE8(s32 arg0, s32 arg1) {
    u8 sp1F;

    sp1F = func_801DC2AC_606D2C(arg0, 0x3E4CCCCD);
    func_801F4584_61F004(arg0);
    func_801F45D0_61F050(arg0);
    if ((func_801D8660_6030E0(arg1, 0xC2200000) == 0.0f) && (sp1F != 0)) {
        func_801EB0CC_615B4C(arg0);
    }
}
