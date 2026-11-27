#include "m2c_types.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
f32 func_801D2F40_5FE320(void *, M2C_UNK);          /* extern */
M2C_UNK func_801D31CC_5FE5AC(s32, M2C_UNK *);       /* extern */
M2C_UNK func_801D3B18_5FEEF8(s32, f32, M2C_UNK);    /* extern */
M2C_UNK func_801D3F00_5FF2E0(s32, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_801F703C_62241C();                     /* extern */
M2C_UNK func_801F732C_62270C(s32);                  /* extern */
M2C_UNK func_801F76D0_622AB0(s32);                     /* extern */
extern M2C_UNK D_8020B2A8_636688;
extern M2C_UNK func_801F3254_61E634;

void func_801F31A0_61E580(s32 arg0, void *arg1) {
    func_801F76D0_622AB0(arg0);
    func_801D3B18_5FEEF8(arg0, M2C_FIELD(arg1, f32 *, 0x20) * 300.0f, 0x10);
    func_801D3F00_5FF2E0(arg0, 0, 8);
    func_801F732C_62270C(arg0);
    if (func_801D2F40_5FE320(arg1, 0x42480000) == 0.0f) {
        func_801F703C_62241C();
        func_801D31CC_5FE5AC(arg0, &D_8020B2A8_636688);
        func_8003521C_35E1C(&func_801F3254_61E634);
    }

    *(volatile s32 *)0x80000000 = 1;
}
