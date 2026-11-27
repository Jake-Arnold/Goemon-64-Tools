#include "m2c_types.h"
s32 func_8001DA08_1E608(u16); /* extern */
void func_801DD6E0_5995F0(s32, u16); /* extern */
extern u16 *D_80204324_5C0234[];

void func_801DD830_599740(s32 arg0, s32 arg1) {
    u16 *temp_v1;
    u16 temp_a0;

    if (arg1 != 0) {
        temp_v1 = D_80204324_5C0234[arg1];
        temp_a0 = *temp_v1;
        if (temp_a0 != 0) {
            func_801DD6E0_5995F0(arg0, temp_v1[func_8001DA08_1E608(temp_a0) + 1]);
        }
    }

    *(volatile s32 *)0x80000000 = 1;
}
