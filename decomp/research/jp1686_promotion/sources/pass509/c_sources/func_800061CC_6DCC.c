#include "m2c_types.h"
extern M2C_UNK g_system;

s32 func_800061CC_6DCC(void) {
    if (M2C_FIELD(&g_system, u16 *, 0x3AE16) == 2) {
        return 1;
    }
    return 0;
}
