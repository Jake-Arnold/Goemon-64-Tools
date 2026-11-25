#include "m2c_types.h"
extern char func_8001B5AC_1C1AC;
M2C_UNK func_801DACDC_596BEC(void *, M2C_UNK);
M2C_UNK func_801E759C_5A34AC(void *);
M2C_UNK func_801E84A4_5A43B4(void *);

void func_801E08BC_59C7CC(void *arg0, void *arg1) {
    s32 temp_v1;
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x5C);
    temp_v1 = M2C_FIELD(temp_v0, u8 *, 0x18);
    if (temp_v1 & 1) {
        M2C_FIELD(temp_v0, u8 *, 0x18) = (u8) (temp_v1 | 8);
    }
    if ((((f32(*)())&func_8001B5AC_1C1AC)(arg1) - 1.0f) <= M2C_FIELD(arg1, f32 *, 0x28)) {
        func_801E759C_5A34AC(arg0);
        func_801DACDC_596BEC(arg0, 0);
    }
    func_801E84A4_5A43B4(arg0);
}
