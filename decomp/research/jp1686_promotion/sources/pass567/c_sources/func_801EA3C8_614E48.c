#include "../m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D8BF0_603670(s32, M2C_UNK *, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_801EA418_614E98();                     /* static */
M2C_UNK func_801F49B0_61F430();                     /* static */
extern M2C_UNK D_802107C4_63B244;

void func_801EA3C8_614E48(void *arg0, s32 arg1) {
    func_801F49B0_61F430();
    M2C_FIELD(arg0, s32 *, 0xB0) = 0;
    func_801D8BF0_603670(arg1, &D_802107C4_63B244, 0, 1);
    func_80034E8C_35A8C(func_801EA418_614E98);
}
