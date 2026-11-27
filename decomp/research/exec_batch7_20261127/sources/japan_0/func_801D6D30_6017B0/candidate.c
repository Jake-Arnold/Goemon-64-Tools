#include "m2c_types.h"
extern u8 *D_80214600_63F080;

void func_801D6D30_6017B0(s16 arg0, s8 arg1) {
    u8 *temp_v0;

    temp_v0 = D_80214600_63F080 + 0x1B0;
    M2C_FIELD(temp_v0, s16 *, 2) = 0;
    M2C_FIELD(temp_v0, s16 *, 4) = 0;
    M2C_FIELD(temp_v0, s16 *, 6) = 0;
    M2C_FIELD(temp_v0, s16 *, 8) = arg0;
    M2C_FIELD(temp_v0, s8 *, 0xA) = 1;
    M2C_FIELD(temp_v0, s8 *, 0xB) = arg1;
    M2C_FIELD(temp_v0, s8 *, 0) = 1;
}
