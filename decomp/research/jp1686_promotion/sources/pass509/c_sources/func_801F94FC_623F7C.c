#include "m2c_types.h"
s32 func_801D9620_6040A0(s32, M2C_UNK, M2C_UNK);    /* extern */
s32 func_801DC2E8_606D68(s32, M2C_UNK);             /* extern */
M2C_UNK func_801F5C70_6206F0(s32);                  /* static */
M2C_UNK func_801FCE00_627880();                     /* static */

void func_801F94FC_623F7C(s32 arg0, M2C_UNK arg1) {
    func_801FCE00_627880();
    if ((func_801DC2E8_606D68(arg0, 0x3DCCCCCD) != 0) && (func_801D9620_6040A0(arg0, 0, 8) != 0)) {
        func_801F5C70_6206F0(arg0);
    }
}
