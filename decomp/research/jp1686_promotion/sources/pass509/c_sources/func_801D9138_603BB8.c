#include "m2c_types.h"
extern void *D_80214600_63F080;

s32 func_801D9138_603BB8(void) {
    if (M2C_FIELD(D_80214600_63F080, s32 *, 0x60) <= 0) {
        M2C_FIELD(D_80214600_63F080, s32 *, 0x60) = 0;
        return 1;
    }
    return 0;
}
