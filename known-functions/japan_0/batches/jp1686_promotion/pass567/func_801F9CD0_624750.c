#include "../m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D8604_603084(s32, M2C_UNK *);       /* extern */
M2C_UNK func_801F9D84_624804();                     /* static */
M2C_UNK func_801FC7A4_627224();                     /* static */
M2C_UNK func_801FCE00_627880(s32);                  /* static */
extern M2C_UNK D_802109F8_63B478;

void func_801F9CD0_624750(s32 arg0, s32 arg1) {
    func_801FC7A4_627224();
    func_801FCE00_627880(arg0);
    func_801D8604_603084(arg1, &D_802109F8_63B478);
    func_80034E8C_35A8C(func_801F9D84_624804);
}
