#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D8738_6031B8(M2C_UNK, M2C_UNK);     /* extern */
M2C_UNK func_801D88EC_60336C(s32, M2C_UNK *);       /* extern */
M2C_UNK func_801D9620_6040A0(s32, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_801F5AC8_620548();                     /* static */
s32 func_801FCA5C_6274DC(s32);                      /* static */
M2C_UNK func_801FCE00_627880(s32);                  /* static */
extern M2C_UNK D_802109D8_63B458;

void func_801F5A60_6204E0(s32 arg0, M2C_UNK arg1) {
    func_801D8738_6031B8(arg1, 0x42200000);
    func_801FCE00_627880(arg0);
    func_801D9620_6040A0(arg0, 0, 8);
    if (func_801FCA5C_6274DC(arg0) != 0) {
        func_801D88EC_60336C(arg0, &D_802109D8_63B458);
        func_80034E8C_35A8C(func_801F5AC8_620548);
    }
}
