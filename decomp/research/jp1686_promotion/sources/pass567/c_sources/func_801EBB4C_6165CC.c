#include "../m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D88EC_60336C(s32, M2C_UNK *);       /* extern */
M2C_UNK func_801D8BF0_603670(s32, M2C_UNK *, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_801EBBA4_616624();                     /* static */
M2C_UNK func_801F4998_61F418();                     /* static */
extern M2C_UNK D_802107C4_63B244;
extern M2C_UNK D_802108E8_63B368;

void func_801EBB4C_6165CC(s32 arg0, s32 arg1) {
    func_801F4998_61F418();
    func_801D88EC_60336C(arg0, &D_802108E8_63B368);
    func_801D8BF0_603670(arg1, &D_802107C4_63B244, 0, 1);
    func_80034E8C_35A8C(func_801EBBA4_616624);
}
