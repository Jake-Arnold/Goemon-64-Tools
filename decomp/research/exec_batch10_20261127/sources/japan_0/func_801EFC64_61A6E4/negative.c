#include "m2c_types.h"
M2C_UNK func_8000EC10_F810(void *, s32, s32, f32, s32);
M2C_UNK func_80034C90_35890(void);
s32 func_801D8D7C_6037FC(void *);
s32 func_801D8DEC_60386C(void *);
M2C_UNK func_801D8FB4_603A34(void *);
M2C_UNK func_801DB86C_6062EC(void *, void *);
M2C_UNK func_801EFD44_61A7C4(void *);

void func_801EFC64_61A6E4(void *arg0, void *arg1) {
    func_801DB86C_6062EC(arg0, arg1);
    M2C_FIELD(arg0, s32 *, 0x94) += 0xA;
    func_8000EC10_F810(arg1, M2C_FIELD(arg0, s32 *, 0x70), M2C_FIELD(arg0, s32 *, 0x74), M2C_FIELD(arg0, f32 *, 0x78), M2C_FIELD(arg0, s32 *, 0x94));
    if (M2C_FIELD(arg0, f32 *, 0x78) < 0.0f) {
        if (--M2C_FIELD(arg0, s32 *, 0x7C) < 0) {
            func_80034C90_35890();
            return;
        }
    }
    if (M2C_FIELD(arg1, f32 *, 0x10) > 0.0f) {
        func_80034C90_35890();
        return;
    }
    if ((func_801D8D7C_6037FC(arg0) != 0) || (func_801D8DEC_60386C(arg0) != 0)) {
        func_801EFD44_61A7C4(arg0);
    }
    func_801D8FB4_603A34(arg0);

    *(volatile s32 *)0x80000000 = 1;
}
