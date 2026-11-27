#include "m2c_types.h"
void func_801CBD88_587C98(void); /* extern */
extern u8 D_3AE23[];
extern s32 D_8015C5C8_15D1C8;

void func_801FAD8C_5B6C9C(void) {
    func_801CBD88_587C98();
    D_3AE23[D_8015C5C8_15D1C8] = 1;

    *(volatile s32 *)0x80000000 = 1;
}
