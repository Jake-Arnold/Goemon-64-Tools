#include "m2c_types.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_80037C20_38820(M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_80037C9C_3889C(M2C_UNK, M2C_UNK);      /* extern */
M2C_UNK func_80038BC8_397C8(M2C_UNK);               /* extern */
f32 func_801D2F40_5FE320(void *, M2C_UNK);          /* extern */
M2C_UNK func_801D31CC_5FE5AC(void *, M2C_UNK *);    /* extern */
M2C_UNK func_801E0950_60BD30(M2C_UNK, s32, f32, s32); /* extern */
M2C_UNK func_801E1084_60C464(void *, s32, f32, s32); /* extern */
M2C_UNK func_801F76D0_622AB0(void *);                     /* extern */
extern M2C_UNK D_8020B2B0_636690;
extern M2C_UNK func_801EFA88_61AE68;

void func_801EF998_61AD78(void *arg0, void *arg1) {
    func_801F76D0_622AB0(arg0);
    if (func_801D2F40_5FE320(arg1, 0xC3960000) == 0.0f) {
        func_801D31CC_5FE5AC(arg0, &D_8020B2B0_636690);
        func_80038BC8_397C8(0x4A);
        func_801E1084_60C464(arg0, M2C_FIELD(arg1, s32 *, 8), M2C_FIELD(arg1, f32 *, 0xC) + 50.0f, M2C_FIELD(arg1, s32 *, 0x10));
        func_801E0950_60BD30(1, M2C_FIELD(arg1, s32 *, 8), M2C_FIELD(arg1, f32 *, 0xC), M2C_FIELD(arg1, s32 *, 0x10));
        func_80037C9C_3889C(0, 0x78);
        func_80037C20_38820(0, 1, 0xAAAAAAAA);
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x78;
        M2C_FIELD(arg0, s32 *, 0x80) = 0;
        func_8003521C_35E1C(&func_801EFA88_61AE68);
    }
    M2C_FIELD(arg1, f32 *, 0xC) = (f32) (M2C_FIELD(arg1, f32 *, 0xC) + 1.0f);
}
