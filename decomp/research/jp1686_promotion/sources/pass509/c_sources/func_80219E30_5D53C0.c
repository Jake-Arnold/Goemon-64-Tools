#include "m2c_types.h"
M2C_UNK func_800370B8_37CB8();                      /* extern */
s32 func_80226164_5E16F4();                         /* extern */

void func_80219E30_5D53C0(void *arg0, M2C_UNK arg1) {
    if ((func_80226164_5E16F4() != 1) && (M2C_FIELD(arg0, s32 *, 0xB4) != 0)) {
        func_800370B8_37CB8();
    }
}
