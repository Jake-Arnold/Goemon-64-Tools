#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
M2C_UNK func_80038838_39438(M2C_UNK);               /* extern */
s32 func_801D8D7C_6037FC(void);                     /* extern */
M2C_UNK func_801D8DE4_603864(u8 *);               /* extern */
M2C_UNK func_801DB804_606284(u8 *);               /* extern */
s32 func_801FCA5C_6274DC(u8 *);                   /* extern */
extern u8 *D_80214600_63F080;
extern M2C_UNK func_801F7B48_6225C8;

void func_801F7A7C_6224FC(void *arg0, M2C_UNK arg1) {
    u8 *sp24;

    sp24 = D_80214600_63F080 + 0x140;
    if ((func_801D8D7C_6037FC() == M2C_FIELD(D_80214600_63F080, s32 *, 0x1CC)) && (M2C_FIELD(sp24, u8 *, 0xE) == 0) && (M2C_FIELD(D_80214600_63F080, u8 *, 0x2C5) == 0)) {
        M2C_FIELD(arg0, s32 *, 0x48) = 0;
        M2C_FIELD(arg0, u8 *, 0x30) &= ~2;
        func_80038838_39438(0x24A);
    }
    func_801D8DE4_603864(arg0);
    if (--M2C_FIELD(arg0, s32 *, 0x7C) < 0) {
        M2C_FIELD(arg0, s32 *, 0x48) = 0;
        M2C_FIELD(arg0, u8 *, 0x30) &= ~2;
        func_801DB804_606284(arg0);
        if (func_801FCA5C_6274DC(arg0) != 0) {
            func_80034E8C_35A8C(&func_801F7B48_6225C8);
        }
    }
}
