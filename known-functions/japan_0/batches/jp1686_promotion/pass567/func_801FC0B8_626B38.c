#include "../m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D88EC_60336C(void *, M2C_UNK *);    /* extern */
M2C_UNK func_801FC110_626B90();                     /* static */
M2C_UNK func_801FC76C_6271EC();                     /* static */
M2C_UNK func_801FC7A4_627224(void *);               /* static */
extern M2C_UNK D_802109D8_63B458;

void func_801FC0B8_626B38(void *arg0, M2C_UNK arg1) {
    func_801FC76C_6271EC();
    func_801FC7A4_627224(arg0);
    func_801D88EC_60336C(arg0, &D_802109D8_63B458);
    M2C_FIELD(arg0, s32 *, 0xEC) = (s32) (M2C_FIELD(arg0, s32 *, 0xEC) + 1);
    func_80034E8C_35A8C(func_801FC110_626B90);
}
