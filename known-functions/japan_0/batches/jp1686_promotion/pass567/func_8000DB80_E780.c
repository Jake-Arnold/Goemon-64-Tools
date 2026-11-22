#include "../m2c_types.h"
s32 func_8000DB18_E718(M2C_UNK);                    /* extern */

s32 func_8000DB80_E780(void) {
    if (func_8000DB18_E718(0x64) >= 0x32) {
        return 1;
    }
    return 0;
}
