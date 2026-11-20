#include "m2c_types.h"
M2C_UNK func_801D8910_603390(M2C_UNK, M2C_UNK);              /* extern */
M2C_UNK func_801F5C70_6206F0(s32);                  /* static */
M2C_UNK func_801FC9E4_627464(s32, M2C_UNK, M2C_UNK); /* static */
extern void *D_80214600_63F080;

void func_801F4FF8_61FA78(s32 arg0, M2C_UNK arg1) {
    func_801D8910_603390(arg0, 0x42200000);
    func_801FC9E4_627464(arg0, 0x3CA3D70A, 0x3ECCCCCD);
    if (M2C_FIELD(D_80214600_63F080, u8 *, 0x2C0) == 0) {
        func_801F5C70_6206F0(arg0);
    }
}
