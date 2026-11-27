#include "m2c_types.h"
M2C_UNK func_8000E39C_EF9C(f32, f32, s32, M2C_UNK, s32); /* extern */
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801D31CC_5FE5AC(s32, M2C_UNK *);       /* extern */
M2C_UNK func_801D34D0_5FE8B0(void *, M2C_UNK *, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_801EF268_61A648(void);                 /* extern */
extern M2C_UNK D_8020B094_636474;
extern M2C_UNK D_8020B178_636558;
extern M2C_UNK func_801E6854_611C34;

void func_801E67D4_611BB4(s32 arg0, void *arg1) {
    func_801EF268_61A648();
    func_801D31CC_5FE5AC(arg0, &D_8020B178_636558);
    func_801D34D0_5FE8B0(arg1, &D_8020B094_636474, 0, 0);
    func_8000E39C_EF9C(10.0f, 0.0f, M2C_FIELD(arg1, s32 *, 0xC), 0xC4834000, arg0);
    func_8003521C_35E1C(&func_801E6854_611C34);
}
