#include "m2c_types.h"
M2C_UNK func_8000F198_FD98(M2C_UNK, s32, void *, M2C_UNK); /* extern */
M2C_UNK func_80034B44_35744();                      /* extern */
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D45B0_5FF030(M2C_UNK);              /* extern */
s32 func_801D8D7C_6037FC(s32);                      /* extern */
s32 func_801D8DEC_60386C(s32);                      /* extern */
M2C_UNK func_801DB86C_6062EC();                     /* extern */
M2C_UNK func_8020A6F4_635174();                     /* static */
M2C_UNK func_8020A974_6353F4(s32, M2C_UNK);         /* static */
extern s32 D_80214600_63F080;

void func_8020A624_6350A4(s32 arg0, void *arg1) {
    func_801DB86C_6062EC();
    if (M2C_FIELD(arg1, f32 *, 0x10) >= 0.0f) {
        func_80034B44_35744();
    }
    if ((func_801D8D7C_6037FC(arg0) != 0) || (func_801D8DEC_60386C(arg0) != 0)) {
        func_8000F198_FD98(0x106, D_80214600_63F080 + 0xA0, arg1, 0x44BB8000);
        func_801D45B0_5FF030(0xA);
        func_8020A974_6353F4(arg0, 0x40400000);
        func_8020A974_6353F4(arg0, 0x40400000);
        func_8020A974_6353F4(arg0, 0x40400000);
        func_8020A974_6353F4(arg0, 0x40400000);
        func_80034E8C_35A8C(func_8020A6F4_635174);
    }
}
