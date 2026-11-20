#include "m2c_types.h"
M2C_UNK func_801D8738_6031B8(M2C_UNK, M2C_UNK);     /* extern */
M2C_UNK func_801DB350_605DD0(void *, s32, s32, s32, s32); /* extern */
s32 func_801DB4B8_605F38(void *, M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
u8 func_801DC36C_606DEC(void *, M2C_UNK);           /* extern */
M2C_UNK func_80201B2C_62C5AC(void *);               /* static */
extern void *func_80214670_5CFC00;

void func_80205074_62FAF4(void *arg0, M2C_UNK arg1) {
    u8 sp2F;

    func_801D8738_6031B8(arg1, 0x42700000);
    M2C_FIELD(func_80214670_5CFC00, s8 *, 0x816) = 2;
    sp2F = func_801DC36C_606DEC(arg0, 0x3ECCCCCD);
    func_801DB350_605DD0(arg0, M2C_FIELD(arg0, s32 *, 0x70), M2C_FIELD(arg0, s32 *, 0x78), func_801DB4B8_605F38(arg0, 0x30, 0x41200000, 0x41000000) & 0xFFFF, 0);
    if (sp2F != 0) {
        if (M2C_FIELD(arg0, s32 *, 0xEC) > 0) {
            M2C_FIELD(arg0, s32 *, 0xEC) = 0;
            M2C_FIELD(arg0, s32 *, 0xD4) = 0;
        }
        func_80201B2C_62C5AC(arg0);
    }
}
