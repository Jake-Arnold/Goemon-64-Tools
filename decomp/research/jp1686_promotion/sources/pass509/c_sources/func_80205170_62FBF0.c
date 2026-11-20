#include "m2c_types.h"
M2C_UNK func_801D8738_6031B8(M2C_UNK, M2C_UNK);     /* extern */
M2C_UNK func_80201B2C_62C5AC(void *);               /* static */
extern s32 D_80214600_63F080;
extern void *func_80214670_5CFC00;

void func_80205170_62FBF0(void *arg0, M2C_UNK arg1) {
    void *sp1C;

    sp1C = D_80214600_63F080 + 0x140;
    M2C_FIELD(func_80214670_5CFC00, s8 *, 0x816) = 2;
    func_801D8738_6031B8(arg1, 0x42700000);
    if (M2C_FIELD(sp1C, u8 *, 0xE) == 3) {
        M2C_FIELD(arg0, s32 *, 0xD4) = 0xA;
        func_80201B2C_62C5AC(arg0);
    }
}
