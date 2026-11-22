#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_802062D4_630D54();                     /* static */
M2C_UNK func_802067B8_631238();                     /* static */
M2C_UNK func_802097AC_63422C(void *);               /* static */
extern void *func_80214670_5CFC00;

void func_80206748_6311C8(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s32 *, 0x7C) = 0x321;
    if ((s32) M2C_FIELD(func_80214670_5CFC00, u8 *, 0x12) <= 0) {
        func_80034E8C_35A8C(func_802062D4_630D54);
    } else {
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x3E8;
        func_80034E8C_35A8C(func_802067B8_631238);
    }
    func_802097AC_63422C(arg0);
}
