#include "m2c_types.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);
M2C_UNK func_801D2EE4_5FE2C4(s32, M2C_UNK *);
f32 func_801D31F0_5FE5D0(M2C_UNK, M2C_UNK);
extern M2C_UNK D_8020B170_636550;
extern u8 *D_8020EED0_63A2B0;
extern M2C_UNK func_801E52D8_6106B8;

void func_801E8108_6134E8(M2C_UNK arg0, s32 arg1) {
    u8 *temp_v0;

    temp_v0 = D_8020EED0_63A2B0 + 0x1B0;
    if (M2C_FIELD(temp_v0, u16 *, 8) != 0) {
        M2C_FIELD(temp_v0, u16 *, 8)--;
    }
    if (func_801D31F0_5FE5D0(arg0, 0x42C80000) == 0.0f && M2C_FIELD(temp_v0, u16 *, 8) == 0) {
        func_801D2EE4_5FE2C4(arg1, &D_8020B170_636550);
        func_8003521C_35E1C(&func_801E52D8_6106B8);
    }
}
