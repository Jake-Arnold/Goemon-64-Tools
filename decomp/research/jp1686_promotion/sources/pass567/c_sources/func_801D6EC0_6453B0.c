#include "../m2c_types.h"
void func_801D6EC0_6453B0(void *arg0, s16 *arg1) {
    M2C_FIELD(arg0, s8 *, 0xA0) = 1;
    *arg1 |= 0x400;
    M2C_FIELD(arg0, s8 *, 0xC5) = 2;
    M2C_FIELD(arg0, s32 *, 0xB8) = 0;
    M2C_FIELD(arg0, s8 *, 0x9F) = (s8) (M2C_FIELD(arg0, s8 *, 0x9F) & 0xFFFB);
}
