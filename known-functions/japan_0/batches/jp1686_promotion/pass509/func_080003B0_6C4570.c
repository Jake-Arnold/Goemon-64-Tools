#include "m2c_types.h"
void func_080003B0_6C4570(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, s32 *, 0x68) & 0x20000) {
        if (M2C_FIELD(arg0, s32 *, 0xD0) == 1) {
            M2C_FIELD(arg0, s32 *, 0x60) = 0;
            return;
        }
        M2C_FIELD(arg0, s32 *, 0x60) = 0x20;
        return;
    }
    if (M2C_FIELD(arg0, s32 *, 0xD0) == 1) {
        M2C_FIELD(arg0, s32 *, 0x60) = 0x80000000;
        return;
    }
    M2C_FIELD(arg0, s32 *, 0x60) = 0x80000020;
}
