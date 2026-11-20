#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_80038838_39438(M2C_UNK);               /* extern */
M2C_UNK func_801D8604_603084(void *, M2C_UNK *);    /* extern */
M2C_UNK func_801D8BF0_603670(void *, M2C_UNK *, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_801ED950_6183D0();                     /* static */
extern M2C_UNK D_802107C4_63B244;
extern M2C_UNK D_802108B0_63B330;
extern M2C_UNK D_802108C0_63B340;

void func_801ED8BC_61833C(void *arg0, void *arg1) {
    M2C_FIELD(arg0, s32 *, 0xB0) = 1;
    func_80038838_39438(0x823E);
    func_80038838_39438(0x8240);
    func_80038838_39438(0x8241);
    if ((s32) M2C_FIELD(arg1, u16 *, 0x16) < 0x201) {
        func_801D8604_603084(arg1, &D_802108C0_63B340);
    } else {
        func_801D8604_603084(arg1, &D_802108B0_63B330);
    }
    func_801D8BF0_603670(arg1, &D_802107C4_63B244, 0, 1);
    func_80034E8C_35A8C(func_801ED950_6183D0);
}
