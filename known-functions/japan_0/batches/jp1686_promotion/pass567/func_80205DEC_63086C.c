#include "../m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_80205E28_6308A8();                     /* static */
M2C_UNK func_802097AC_63422C(void *);               /* static */

void func_80205DEC_63086C(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s32 *, 0x7C) = 0xFA;
    func_80034E8C_35A8C(func_80205E28_6308A8);
    func_802097AC_63422C(arg0);
}
