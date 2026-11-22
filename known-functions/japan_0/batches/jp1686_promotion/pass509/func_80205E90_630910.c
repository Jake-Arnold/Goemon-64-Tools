#include "m2c_types.h"
M2C_UNK func_801DA314_604D94(s32, M2C_UNK);         /* extern */
M2C_UNK func_80205DB4_630834(s32);                  /* static */
M2C_UNK func_802097AC_63422C(s32);                  /* static */
M2C_UNK func_80209D54_6347D4();                     /* static */
extern s32 D_80214600_63F080;
extern void *func_80214670_5CFC00;

void func_80205E90_630910(s32 arg0, s32 arg1) {
    void *sp1C;

    sp1C = D_80214600_63F080 + 0x140;
    func_80209D54_6347D4();
    func_801DA314_604D94(arg1 + 8, 0x3F800000);
    if (M2C_FIELD(sp1C, u8 *, 0xE) != 5) {
        M2C_FIELD(func_80214670_5CFC00, s8 *, 4) = 0;
        func_80205DB4_630834(arg0);
    }
    func_802097AC_63422C(arg0);
}
