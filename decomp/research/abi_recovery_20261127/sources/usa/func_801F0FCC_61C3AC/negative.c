#include "m2c_types.h"
f32 func_80003E10_4A10(u16);                        /* extern */
f32 func_80003EA0_4AA0(u16);                        /* extern */
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801D31CC_5FE5AC(void *, M2C_UNK *);    /* extern */
M2C_UNK func_801F76D0_622AB0(void *);                     /* extern */
extern M2C_UNK D_8020B288_636668;
extern M2C_UNK func_801F1074_61C454;

void func_801F0FCC_61C3AC(void *arg0, void *arg1) {
    func_801F76D0_622AB0(arg0);
    func_801D31CC_5FE5AC(arg0, &D_8020B288_636668);
    M2C_FIELD(arg0, f32 *, 0x74) = 9.0f;
    M2C_FIELD(arg0, f32 *, 0x70) = (f32) ((f64) func_80003E10_4A10(M2C_FIELD(arg1, u16 *, 0x16)) * 3.0);
    M2C_FIELD(arg0, f32 *, 0x78) = (f32) ((f64) func_80003EA0_4AA0(M2C_FIELD(arg1, u16 *, 0x16)) * 3.0);
    func_8003521C_35E1C(&func_801F1074_61C454);

    *(volatile s32 *)0x80000000 = 1;
}
