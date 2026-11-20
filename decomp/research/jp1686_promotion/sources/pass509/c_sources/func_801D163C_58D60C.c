#include "m2c_types.h"
M2C_UNK func_801D1BC0_58DB90(void *, s32, s32);     /* extern */
M2C_UNK func_801D2734_58E704(void *);               /* extern */
M2C_UNK func_801E019C_59C16C(void *, M2C_UNK);      /* extern */
s32 func_801ECFB8_5A8F88(void *);                   /* extern */
M2C_UNK func_801FBECC_5B7E9C(void *);               /* extern */
M2C_UNK func_801D16CC_58D69C(void *);               /* static */
M2C_UNK func_801D1700_58D6D0();                     /* static */

void func_801D163C_58D60C(void *arg0) {
    func_801D1700_58D6D0();
    func_801D16CC_58D69C(arg0);
    func_801D1BC0_58DB90(arg0, M2C_FIELD(arg0, s32 *, 0xE4), M2C_FIELD(arg0, s32 *, 0xE8));
    func_801D2734_58E704(arg0);
    if (func_801ECFB8_5A8F88(arg0) != 0) {
        func_801FBECC_5B7E9C(arg0);
        func_801E019C_59C16C(arg0, 0xAE);
        return;
    }
    if (M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), u16 *, 0x86) == 0) {
        func_801E019C_59C16C(arg0, 0);
    }
}
