#include "../m2c_types.h"
void func_801D6D60_645250(void *arg0, s16 *arg1) {
    s8 temp_v0;

    temp_v0 = M2C_FIELD(arg0, s8 *, 0xA2) - 1;
    M2C_FIELD(arg0, s8 *, 0xA2) = temp_v0;
    if (temp_v0 == 0) {
        M2C_FIELD(arg0, s8 *, 0x9E) = 2;
        *arg1 |= 0x4000;
    }
}
