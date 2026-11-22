#include "../m2c_types.h"
M2C_UNK func_801DB86C_6062EC();                     /* static */

s32 func_801DB290_605D10(void *arg0) {
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, s32 *, 0x7C);
    if (temp_v0 != 0) {
        M2C_FIELD(arg0, s32 *, 0x7C) = (s32) (temp_v0 - 1);
        func_801DB86C_6062EC();
        return 0;
    }
    return 1;
}
