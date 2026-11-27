#include "m2c_types.h"
s32 func_8000DD58_E958(M2C_UNK);                    /* extern */
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
s32 func_801D3B18_5FEEF8(void *, f32, M2C_UNK);             /* extern */
M2C_UNK func_80203BC0_62EFA0(void *, s32);          /* extern */
M2C_UNK func_80205C00_630FE0(void *);               /* extern */
extern void *D_8020EF40_63A320;
extern M2C_UNK func_8020580C_630BEC;
extern M2C_UNK func_802058B0_630C90;

void func_80205734_630B14(void *arg0, void *arg1) {
    if (func_801D3B18_5FEEF8(arg0, M2C_FIELD(arg1, f32 *, 0x20) * 100.0f, 0xA) != 0) {
        func_80203BC0_62EFA0(arg0, ((func_8000DD58_E958(0x28) / 10) + 0x12) & 0xFF);
        M2C_FIELD(arg0, s32 *, 0x7C) = (s32) (func_8000DD58_E958(0x64) + 0x50);
        M2C_FIELD(arg0, s32 *, 0x80) = 0x96;
        func_8003521C_35E1C(&func_8020580C_630BEC);
    }
    if (M2C_FIELD(D_8020EF40_63A320, u8 *, 0x11) == 2) {
        func_8003521C_35E1C(&func_802058B0_630C90);
        M2C_FIELD(arg0, s32 *, 0x88) = (s32) (M2C_FIELD(arg0, s32 *, 0x84) * 0x1E);
    }
    func_80205C00_630FE0(arg0);

    *(volatile s32 *)0x80000000 = 1;
}
