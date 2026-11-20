#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_80205DB4_630834(void *);               /* static */
M2C_UNK func_8020703C_631ABC();                     /* static */
M2C_UNK func_802097AC_63422C(void *);               /* static */
extern void *func_80214670_5CFC00;

void func_80206FE4_631A64(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s32 *, 0x7C) = 0x15E;
    func_80034E8C_35A8C(func_8020703C_631ABC);
    if (M2C_FIELD(func_80214670_5CFC00, u8 *, 0xE) != 0) {
        func_80205DB4_630834(arg0);
    }
    func_802097AC_63422C(arg0);
}
