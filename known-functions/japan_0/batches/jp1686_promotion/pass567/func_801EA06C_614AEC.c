#include "../m2c_types.h"
M2C_UNK func_801D898C_60340C(s32, M2C_UNK);         /* extern */
M2C_UNK func_801F49B0_61F430();                     /* static */
extern void *D_80214600_63F080;

void func_801EA06C_614AEC(s32 arg0, M2C_UNK arg1) {
    func_801F49B0_61F430();
    M2C_FIELD(D_80214600_63F080, s8 *, 0x2C1) = 0;
    func_801D898C_60340C(arg0, 0x42200000);
}
