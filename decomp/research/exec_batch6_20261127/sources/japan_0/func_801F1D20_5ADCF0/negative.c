#include "m2c_types.h"
void *func_801EE010_5A9FE0(void *, u8); /* extern */
void func_801F2248_5AE218(void *); /* extern */

void func_801F1D20_5ADCF0(void *arg0, u8 arg1) {
    void *temp_v0;

    temp_v0 = func_801EE010_5A9FE0(arg0, arg1);
    if (temp_v0 != NULL) {
        func_801F2248_5AE218(temp_v0);
    }

    *(volatile s32 *)0x80000000 = 1;
}
