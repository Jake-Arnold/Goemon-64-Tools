#include "m2c_types.h"
M2C_UNK func_80034E9C_35A9C(void *, M2C_UNK (*)()); /* extern */
M2C_UNK func_801D88EC_60336C(void *, M2C_UNK *);    /* extern */
M2C_UNK func_801F5AF4_620574();                     /* static */
M2C_UNK func_801F5BAC_62062C();                     /* static */
M2C_UNK func_801FC734_6271B4();                     /* static */
M2C_UNK func_801FC7A4_627224(void *);               /* static */
s32 func_801FC90C_62738C();                         /* static */
extern M2C_UNK D_80210990_63B410;

void func_801F5C70_6206F0(void *arg0) {
    M2C_FIELD(arg0, s32 *, 0xD8) = 0;
    M2C_FIELD(arg0, s32 *, 0xE0) = 0;
    func_801FC734_6271B4();
    func_801FC7A4_627224(arg0);
    func_801D88EC_60336C(arg0, &D_80210990_63B410);
    if (func_801FC90C_62738C() == 0) {
        func_80034E9C_35A9C(arg0, func_801F5AF4_620574);
        return;
    }
    func_80034E9C_35A9C(arg0, func_801F5BAC_62062C);
}
