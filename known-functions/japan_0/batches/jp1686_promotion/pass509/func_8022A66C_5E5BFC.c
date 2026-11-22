#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_8021EBE0_5DA170(void *, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_802213C4_5DC954(void *);               /* extern */
s32 func_8022A118_5E56A8();                         /* static */
M2C_UNK func_8022A62C_5E5BBC();                     /* static */

void func_8022A66C_5E5BFC(void *arg0, M2C_UNK arg1) {
    if (func_8022A118_5E56A8() != 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = 0x02A007E1;
        func_802213C4_5DC954(arg0);
        func_8021EBE0_5DA170(arg0, 5, 0);
        func_80034E8C_35A8C(func_8022A62C_5E5BBC);
    }
}
