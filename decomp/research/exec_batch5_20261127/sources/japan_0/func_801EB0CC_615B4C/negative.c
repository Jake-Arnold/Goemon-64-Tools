#include "m2c_types.h"
M2C_UNK func_80034E9C_35A9C(void *, M2C_UNK *);
M2C_UNK func_801D88EC_60336C(void *, M2C_UNK *);
M2C_UNK func_801D8C54_6036D4(void *, M2C_UNK *, M2C_UNK);
extern M2C_UNK D_802107C4_63B244;
extern M2C_UNK D_802108A0_63B320;
extern M2C_UNK func_801EAA08_615488;

void func_801EB0CC_615B4C(void *arg0) {
    M2C_FIELD(arg0, s32 *, 0xD8) = 0;
    func_801D88EC_60336C(arg0, &D_802108A0_63B320);
    func_801D8C54_6036D4(arg0, &D_802107C4_63B244, 0);
    func_80034E9C_35A9C(arg0, &func_801EAA08_615488);

    *(volatile s32 *)0x80000000 = 1;
}
