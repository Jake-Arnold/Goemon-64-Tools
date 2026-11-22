#include "m2c_types.h"
M2C_UNK func_801E019C_59C16C(s32, M2C_UNK);         /* extern */
M2C_UNK func_801EB500_5A74D0();                     /* extern */

void func_801E5400_5A13D0(s32 arg0, void *arg1) {
    if ((f64) M2C_FIELD(arg1, f32 *, 0x28) <= 0.0) {
        func_801EB500_5A74D0();
        func_801E019C_59C16C(arg0, 0);
    }
}
