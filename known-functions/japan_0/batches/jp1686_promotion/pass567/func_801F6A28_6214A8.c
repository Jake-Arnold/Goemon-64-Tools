#include "../m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D88EC_60336C(s32, M2C_UNK *);       /* extern */
M2C_UNK func_801F6A70_6214F0();                     /* static */
M2C_UNK func_801FC7A4_627224();                     /* static */
M2C_UNK func_801FCE00_627880(s32);                  /* static */
extern M2C_UNK D_80210998_63B418;

void func_801F6A28_6214A8(s32 arg0, M2C_UNK arg1) {
    func_801FC7A4_627224();
    func_801FCE00_627880(arg0);
    func_801D88EC_60336C(arg0, &D_80210998_63B418);
    func_80034E8C_35A8C(func_801F6A70_6214F0);
}
