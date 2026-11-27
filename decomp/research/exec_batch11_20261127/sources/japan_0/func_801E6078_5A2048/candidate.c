#include "m2c_types.h"
void func_8001B13C_1BD3C(void);                     /* extern */
void func_801E019C_59C16C(void *, s32);             /* extern */
void func_801E2AD0_59EAA0(void *, s32);             /* extern */

void func_801E6078_5A2048(void *arg0, void *arg1) {
    func_801E2AD0_59EAA0(arg0, 9);
    if ((((f32 (*)(void *))func_8001B13C_1BD3C)(arg1) - 1.0f) <= M2C_FIELD(arg1, f32 *, 0x28)) {
        M2C_FIELD(arg0, u8 *, 0x30) |= 1;
        func_801E019C_59C16C(arg0, 0);
    }
}
