#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D8604_603084(s32, M2C_UNK *);       /* extern */
M2C_UNK func_801F2340_61CDC0();                     /* static */
s32 func_801F260C_61D08C();                         /* static */
extern M2C_UNK D_802108B0_63B330;

void func_801F22F0_61CD70(void *arg0, s32 arg1) {
    if (func_801F260C_61D08C() == 0) {
        M2C_FIELD(arg0, s32 *, 0xA4) = 0xF;
        func_801D8604_603084(arg1, &D_802108B0_63B330);
        func_80034E8C_35A8C(func_801F2340_61CDC0);
    }
}
