#include "../m2c_types.h"
M2C_UNK func_80034E8C_35A8C(s32);                   /* extern */
s32 func_8003EE44_3FA44();                          /* extern */

void func_8022659C_5E1B2C(void *arg0, M2C_UNK arg1) {
    if (func_8003EE44_3FA44() == 0) {
        func_80034E8C_35A8C(M2C_FIELD(arg0, s32 *, 0xBC));
    }
}
