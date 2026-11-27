#include "m2c_types.h"

void func_8003522C_35E2C(void *, void (*)(void));
extern void *D_8020EED0_63A2B0;
void func_801ECD54_618134(void);

s32 func_801ECEDC_6182BC(void *arg0) {
    if (M2C_FIELD(M2C_FIELD(D_8020EED0_63A2B0, void **, 0x1D8), s32 *, 0xD8) != 5) {
        M2C_FIELD(arg0, f32 *, 0xA8) = 8.0f;
        func_8003522C_35E2C(arg0, func_801ECD54_618134);
        return 1;
    }
    return 0;
}
