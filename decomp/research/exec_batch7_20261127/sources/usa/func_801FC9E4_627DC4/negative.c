#include "m2c_types.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);
f32 func_801D2F40_5FE320(void *, f32);
M2C_UNK func_801D31CC_5FE5AC(s32, M2C_UNK *);
s32 func_801D3F00_5FF2E0(s32, s32, s32);
M2C_UNK func_801FFDFC_62B1DC(void);
extern M2C_UNK D_8020B448_636828;
extern M2C_UNK func_801FCA6C_627E4C;

void func_801FC9E4_627DC4(s32 arg0, void *arg1) {
    if ((func_801D3F00_5FF2E0(arg0, 0, 8) != 0) && (func_801D2F40_5FE320(arg1, 30.0f) == 0.0f)) {
        func_801FFDFC_62B1DC();
        func_801D31CC_5FE5AC(arg0, &D_8020B448_636828);
        M2C_FIELD(arg1, f32 *, 0x28) = 10.0f;
        func_8003521C_35E1C(&func_801FCA6C_627E4C);
    }

    *(volatile s32 *)0x80000000 = 1;
}
