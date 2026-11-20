#include "m2c_types.h"
M2C_UNK func_80004170_4D70();                       /* extern */
M2C_UNK func_80009FA0_ABA0();                       /* extern */
M2C_UNK func_8000B6F0_C2F0();                       /* extern */
M2C_UNK func_8000B714_C314(M2C_UNK *);              /* extern */
M2C_UNK func_800134D0_140D0();                      /* extern */
M2C_UNK func_800344FC_350FC(M2C_UNK);               /* extern */
M2C_UNK func_800357C0_363C0();                      /* extern */
M2C_UNK osViBlack(M2C_UNK);                         /* extern */
extern M2C_UNK D_80062A10_63610;
extern M2C_UNK g_system;

void func_800037A4_43A4(void) {
    func_80004170_4D70();
    func_800344FC_350FC(0);
    func_80009FA0_ABA0();
    func_800357C0_363C0();
    func_8000B6F0_C2F0();
    func_8000B714_C314(&D_80062A10_63610);
    M2C_FIELD(&g_system, s16 *, 0x3AE24) = 0x14;
    func_800134D0_140D0();
    osViBlack(0);
}
