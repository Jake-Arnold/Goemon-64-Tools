#include "../m2c_types.h"
s32 func_802190F0_677F60(s32 arg0) {
    void *temp_v1;

    temp_v1 = arg0 + 0x5C;
    if (arg0 == 0) {
        return 0;
    }
    M2C_FIELD(temp_v1, s32 *, 0xC) = 9;
    M2C_FIELD(temp_v1, s32 *, 0x10) = 0;
    M2C_FIELD(temp_v1, s32 *, 0x14) = 0x1C;
    M2C_FIELD(temp_v1, s32 *, 0x18) = 1;
    return 9;
}
