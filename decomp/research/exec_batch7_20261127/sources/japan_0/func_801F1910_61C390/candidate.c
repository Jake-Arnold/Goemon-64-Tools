#include "m2c_types.h"
M2C_UNK func_8000EC10_F810(void *, s32, s32, f32, s32);
M2C_UNK func_80034B44_35744(void);
M2C_UNK func_80034C90_35890(void);
s32 func_801D8D7C_6037FC(void *);
s32 func_801D8DEC_60386C(void *);
M2C_UNK func_801DB86C_6062EC(void);
M2C_UNK func_801E726C_611CEC(void *, f32, s32, s32, f32, f32, f32, f32);

void func_801F1910_61C390(void *arg0, void *arg1) {
    func_801DB86C_6062EC();
    M2C_FIELD(arg0, s32 *, 0x94) += 4;
    func_8000EC10_F810(arg1, M2C_FIELD(arg0, s32 *, 0x70), M2C_FIELD(arg0, s32 *, 0x74), M2C_FIELD(arg0, f32 *, 0x78), M2C_FIELD(arg0, s32 *, 0x94));
    if (M2C_FIELD(arg0, f32 *, 0x78) < 0.0f) {
        if (--M2C_FIELD(arg0, s32 *, 0x7C) < 0) {
            func_80034C90_35890();
            return;
        }
    }
    if (M2C_FIELD(arg1, f32 *, 0x10) >= 0.0f) {
        func_80034B44_35744();
        return;
    }
    if ((func_801D8D7C_6037FC(arg0) != 0) || (func_801D8DEC_60386C(arg0) != 0)) {
        func_801E726C_611CEC(arg0, M2C_FIELD(arg1, f32 *, 0x1C) * 3.0f, M2C_FIELD(arg1, s32 *, 8), M2C_FIELD(arg1, s32 *, 0xC), M2C_FIELD(arg1, f32 *, 0x10), 0.0f, 0.0f, 0.0f);
    }
}
