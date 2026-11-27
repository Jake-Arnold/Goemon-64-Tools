#include "m2c_types.h"
M2C_UNK func_8000EE50_FA50(void *, s32, s32, f32, s32);
M2C_UNK func_80035020_35C20(void);
s32 func_801D365C_5FEA3C(void *);
s32 func_801D36CC_5FEAAC(void *);
M2C_UNK func_801D3894_5FEC74(void *);
M2C_UNK func_801D614C_60152C(void *, void *);
M2C_UNK func_801EA614_6159F4(void *);

void func_801EA534_615914(void *arg0, void *arg1) {
    func_801D614C_60152C(arg0, arg1);
    M2C_FIELD(arg0, s32 *, 0x94) += 0xA;
    func_8000EE50_FA50(arg1, M2C_FIELD(arg0, s32 *, 0x70), M2C_FIELD(arg0, s32 *, 0x74), M2C_FIELD(arg0, f32 *, 0x78), M2C_FIELD(arg0, s32 *, 0x94));
    if (M2C_FIELD(arg0, f32 *, 0x78) < 0.0f) {
        if (--M2C_FIELD(arg0, s32 *, 0x7C) < 0) {
            func_80035020_35C20();
            return;
        }
    }
    if (M2C_FIELD(arg1, f32 *, 0x10) > 0.0f) {
        func_80035020_35C20();
        return;
    }
    if ((func_801D365C_5FEA3C(arg0) != 0) || (func_801D36CC_5FEAAC(arg0) != 0)) {
        func_801EA614_6159F4(arg0);
    }
    func_801D3894_5FEC74(arg0);
}
