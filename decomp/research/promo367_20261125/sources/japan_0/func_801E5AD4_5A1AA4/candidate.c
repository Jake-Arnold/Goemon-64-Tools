#include "m2c_types.h"
extern char func_8001B13C_1BD3C;
M2C_UNK func_801E019C_59C16C(void *, M2C_UNK);
M2C_UNK func_801EC6C4_5A8694(void *);
M2C_UNK func_801ED5A4_5A9574(void *);

void func_801E5AD4_5A1AA4(void *arg0, void *arg1) {
    s32 temp_v1;
    void *temp_v0;

    temp_v0 = M2C_FIELD(arg0, void **, 0x5C);
    temp_v1 = M2C_FIELD(temp_v0, u8 *, 0x18);
    if (temp_v1 & 1) {
        M2C_FIELD(temp_v0, u8 *, 0x18) = (u8) (temp_v1 | 8);
    }
    if ((((f32(*)())&func_8001B13C_1BD3C)(arg1) - 1.0f) <= M2C_FIELD(arg1, f32 *, 0x28)) {
        func_801EC6C4_5A8694(arg0);
        func_801E019C_59C16C(arg0, 0);
    }
    func_801ED5A4_5A9574(arg0);
}
