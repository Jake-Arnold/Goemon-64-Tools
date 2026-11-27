#include "m2c_types.h"

void func_80034E9C_35A9C(void *, void (*)(void));
extern void *D_80214600_63F080;
void func_801F2484_61CF04(void);

s32 func_801F260C_61D08C(void *arg0) {
    if (M2C_FIELD(M2C_FIELD(D_80214600_63F080, void **, 0x1D8), s32 *, 0xD8) != 5) {
        M2C_FIELD(arg0, f32 *, 0xA8) = 8.0f;
        func_80034E9C_35A9C(arg0, func_801F2484_61CF04);
        { *(volatile s32 *)0x80000000 = 1; } return 1;
    }
    return 0;
}
