#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D8738_6031B8(s32, M2C_UNK);         /* extern */
M2C_UNK func_801DBA50_6064D0(M2C_UNK, M2C_UNK);              /* extern */
M2C_UNK func_801DBB3C_6065BC(s32, M2C_UNK);         /* extern */
M2C_UNK func_8020EF1C_63999C();                     /* static */
extern void *D_80214600_63F080;

void func_8020EEB8_639938(s32 arg0, s32 arg1) {
    func_801DBA50_6064D0(arg0, 0xC25C0000);
    func_801DBB3C_6065BC(arg0, 0xC3FA0000);
    func_801D8738_6031B8(arg1, 0x42700000);
    if (M2C_FIELD(D_80214600_63F080, u8 *, 0x2C1) == 2) {
        func_80034E8C_35A8C(func_8020EF1C_63999C);
    }
}
