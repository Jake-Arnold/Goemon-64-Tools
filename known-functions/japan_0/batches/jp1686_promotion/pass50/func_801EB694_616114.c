#include "m2c_types.h"
f32 func_801D8660_6030E0(s32, M2C_UNK);             /* extern */
M2C_UNK func_801DB350_605DD0(void *, s32, s32, s32, s32); /* extern */
s32 func_801DB4B8_605F38(void *, M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
u8 func_801DC36C_606DEC(void *, M2C_UNK);                   /* extern */
M2C_UNK func_801EB0CC_615B4C(void *);               /* static */
M2C_UNK func_801F4584_61F004(void *);               /* static */
M2C_UNK func_801F45D0_61F050(void *);               /* static */

void func_801EB694_616114(void *arg0, s32 arg1) {
    u8 sp2F;

    sp2F = func_801DC36C_606DEC(arg0, 0x3E4CCCCD);
    func_801F4584_61F004(arg0);
    func_801F45D0_61F050(arg0);
    func_801DB350_605DD0(arg0, M2C_FIELD(arg0, s32 *, 0x70), M2C_FIELD(arg0, s32 *, 0x78), func_801DB4B8_605F38(arg0, 0x30, 0x41200000, 0x41000000) & 0xFFFF, 0);
    if ((func_801D8660_6030E0(arg1, 0xC1A00000) == 0.0f) && (sp2F != 0)) {
        if (M2C_FIELD(arg0, s32 *, 0xEC) >= 2) {
            M2C_FIELD(arg0, s32 *, 0xEC) = 0;
            M2C_FIELD(arg0, s32 *, 0xD4) = 0;
        }
        func_801EB0CC_615B4C(arg0);
    }
}
