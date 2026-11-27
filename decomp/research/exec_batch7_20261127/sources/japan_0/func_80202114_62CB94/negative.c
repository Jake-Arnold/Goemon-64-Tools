#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);
f32 func_801D8660_6030E0(void *, f32);
M2C_UNK func_801D88EC_60336C(s32, M2C_UNK *);
s32 func_801D9620_6040A0(s32, s32, s32);
M2C_UNK func_8020552C_62FFAC(void);
extern M2C_UNK D_80210B78_63B5F8;
extern M2C_UNK func_8020219C_62CC1C;

void func_80202114_62CB94(s32 arg0, void *arg1) {
    if ((func_801D9620_6040A0(arg0, 0, 8) != 0) && (func_801D8660_6030E0(arg1, 30.0f) == 0.0f)) {
        func_8020552C_62FFAC();
        func_801D88EC_60336C(arg0, &D_80210B78_63B5F8);
        M2C_FIELD(arg1, f32 *, 0x28) = 10.0f;
        func_80034E8C_35A8C(&func_8020219C_62CC1C);
    }

    *(volatile s32 *)0x80000000 = 1;
}
