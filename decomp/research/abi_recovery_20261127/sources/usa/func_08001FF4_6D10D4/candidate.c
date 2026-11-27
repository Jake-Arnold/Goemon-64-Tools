#include "m2c_types.h"
extern char func_802268A8_5E1D78;

void func_08001FF4_6D10D4(void *arg0, M2C_UNK arg1) {
    if (((s32  (*)(void *))&func_802268A8_5E1D78)(arg0) != 0) {
        M2C_FIELD(arg0, s32 *, 0x68) = (s32) (M2C_FIELD(arg0, s32 *, 0x68) | 2);
    }
}
