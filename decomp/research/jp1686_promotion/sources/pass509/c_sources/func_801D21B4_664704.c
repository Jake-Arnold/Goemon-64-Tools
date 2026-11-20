#include "m2c_types.h"
M2C_UNK func_80010764_11364(s32, M2C_UNK);          /* extern */
s32 func_80011044_11C44(void *, M2C_UNK, M2C_UNK);  /* extern */
s32 func_80011560_12160(void *, M2C_UNK);           /* extern */
M2C_UNK func_8001B234_1BE34(M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_80022FC0_23BC0();                      /* extern */
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
M2C_UNK func_801D0B90_6630E0();                     /* static */
extern s32 D_801DA2F8_66C848;
extern s32 D_801E7C00_67A150;
extern M2C_UNK func_801D4AEC_66703C;

void func_801D21B4_664704(void *arg0, M2C_UNK arg1) {
    func_80022FC0_23BC0();
    func_801D0B90_6630E0();
    func_80010764_11364(D_801DA2F8_66C848, 0);
    func_8001B234_1BE34(0x64, 0x64, 0x64);
    D_801E7C00_67A150 = func_80011044_11C44(arg0, 2, 0);
    M2C_FIELD(arg0, s32 *, 0xA4) = func_80011560_12160(arg0, 0xB);
    func_80034E8C_35A8C(&func_801D4AEC_66703C);
}
