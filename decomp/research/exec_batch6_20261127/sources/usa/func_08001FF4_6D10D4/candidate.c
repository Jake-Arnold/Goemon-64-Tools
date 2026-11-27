#include "m2c_types.h"
s32 func_802268A8_5E1D78(void *); /* extern */

void func_08001FF4_6D10D4(void *arg0, M2C_UNK arg1) {
    s32 (*fn)(void *) = func_802268A8_5E1D78;
    if (fn(arg0) != 0) {
        M2C_FIELD(arg0, s32 *, 0x68) |= 2;
    }
}
