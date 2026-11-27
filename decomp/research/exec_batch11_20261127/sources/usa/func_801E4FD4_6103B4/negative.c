#include "m2c_types.h"
M2C_UNK func_8000E39C_EF9C(f32, f32, s32, M2C_UNK, void *); /* extern */
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801D31CC_5FE5AC(void *, M2C_UNK *);    /* extern */
M2C_UNK func_801D34D0_5FE8B0(void *, M2C_UNK *, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_801EF280_61A660(void);                 /* extern */
extern M2C_UNK D_8020B094_636474;
extern M2C_UNK D_8020B170_636550;
extern M2C_UNK func_801E5064_610444;

void func_801E4FD4_6103B4(void *arg0, void *arg1) {
    func_801EF280_61A660();
    M2C_FIELD(arg0, s32 *, 0xB0) = 1;
    M2C_FIELD(arg0, s32 *, 0xE0) = 0;
    M2C_FIELD(arg0, s32 *, 0xD8) = 0;
    func_801D31CC_5FE5AC(arg0, &D_8020B170_636550);
    func_801D34D0_5FE8B0(arg1, &D_8020B094_636474, 0, 0);
    func_8000E39C_EF9C(5.0f, 0.0f, M2C_FIELD(arg1, s32 *, 0xC), 0xC3FA0000, arg0);
    func_8003521C_35E1C(&func_801E5064_610444);

    *(volatile int *)0x80000000 = 1;
}
