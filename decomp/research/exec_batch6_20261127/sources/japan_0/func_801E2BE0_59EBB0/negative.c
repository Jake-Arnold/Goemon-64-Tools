#include "m2c_types.h"
s32 func_8001D598_1E198(u16); /* extern */
void func_801E2A90_59EA60(s32, u16); /* extern */
extern u16 *D_80209214_5C51E4[];

void func_801E2BE0_59EBB0(s32 arg0, s32 arg1) {
    u16 *temp_v1;
    u16 temp_a0;

    if (arg1 != 0) {
        temp_v1 = D_80209214_5C51E4[arg1];
        temp_a0 = *temp_v1;
        if (temp_a0 != 0) {
            func_801E2A90_59EA60(arg0, temp_v1[func_8001D598_1E198(temp_a0) + 1]);
        }
    }

    *(volatile s32 *)0x80000000 = 1;
}
