#include "m2c_types.h"
void func_801F32D8_5AF2A8(void *arg0, void *arg1) {
    if ((arg0 != NULL) && (arg1 != NULL)) {
        M2C_FIELD(arg1, u16 *, 0x14) = (u16) M2C_FIELD(arg0, u16 *, 0x14);
        M2C_FIELD(arg1, u16 *, 0x16) = (u16) M2C_FIELD(arg0, u16 *, 0x16);
        M2C_FIELD(arg1, u16 *, 0x18) = (u16) M2C_FIELD(arg0, u16 *, 0x18);
    }
}
