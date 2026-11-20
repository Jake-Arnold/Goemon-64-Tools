#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_80205B64_6305E4();                     /* static */
extern void *D_80214600_63F080;

void func_80205B10_630590(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(D_80214600_63F080, u8 *, 0x2C1) == 1) {
        func_80034E8C_35A8C(func_80205B64_6305E4);
        M2C_FIELD(arg0, f32 *, 0x74) = -1.0f;
    }
}
