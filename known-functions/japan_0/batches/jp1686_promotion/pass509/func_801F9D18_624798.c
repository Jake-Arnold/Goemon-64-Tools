#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D8604_603084(void *, M2C_UNK *);    /* extern */
M2C_UNK func_801F9D84_624804();                     /* static */
M2C_UNK func_801FC7A4_627224();                     /* static */
M2C_UNK func_801FCE00_627880(s32);                  /* static */
extern M2C_UNK D_802109E8_63B468;
extern M2C_UNK D_802109F0_63B470;

void func_801F9D18_624798(s32 arg0, void *arg1) {
    func_801FC7A4_627224();
    func_801FCE00_627880(arg0);
    if ((s32) M2C_FIELD(arg1, u16 *, 0x16) < 0x201) {
        func_801D8604_603084(arg1, &D_802109F0_63B470);
    } else {
        func_801D8604_603084(arg1, &D_802109E8_63B468);
    }
    func_80034E8C_35A8C(func_801F9D84_624804);
}
