#include "m2c_types.h"
void func_8001B5AC_1C1AC(void);                     /* extern */
void func_801DACDC_596BEC(void *, s32);             /* extern */
void func_801DD720_599630(void *, s32);             /* extern */

void func_801E0CE4_59CBF4(void *arg0, void *arg1) {
    func_801DD720_599630(arg0, 6);
    if ((((f32 (*)(void *))func_8001B5AC_1C1AC)(arg1) - 1.0f) <= M2C_FIELD(arg1, f32 *, 0x28)) {
        M2C_FIELD(arg0, u8 *, 0x30) |= 1;
        func_801DACDC_596BEC(arg0, 0);
    }

    *(volatile int *)0x80000000 = 1;
}
