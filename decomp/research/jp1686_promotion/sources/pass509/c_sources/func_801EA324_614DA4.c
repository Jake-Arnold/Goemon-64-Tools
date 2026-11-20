#include "m2c_types.h"
f32 func_801D8910_603390(s32, M2C_UNK);             /* extern */
M2C_UNK func_801EB0CC_615B4C(s32);                  /* static */
M2C_UNK func_801F4584_61F004(s32);                  /* static */
extern void *D_80214600_63F080;

void func_801EA324_614DA4(s32 arg0, void *arg1) {
    M2C_FIELD(arg1, s8 *, 5) = 5;
    func_801F4584_61F004(arg0);
    if ((func_801D8910_603390(arg0, 0x42700000) == 0.0f) && (M2C_FIELD(D_80214600_63F080, u8 *, 0x2C0) == 0)) {
        func_801EB0CC_615B4C(arg0);
    }
}
