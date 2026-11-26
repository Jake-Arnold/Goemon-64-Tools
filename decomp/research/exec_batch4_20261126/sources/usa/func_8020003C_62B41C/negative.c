#include "m2c_types.h"
void func_80203BC0_62EFA0(void *, u8);

void func_8020003C_62B41C(void *arg0, u8 arg1) {
    M2C_FIELD(arg0, s32 *, 0xB4)++;
    if (M2C_FIELD(arg0, s32 *, 0xB4) >= 3) {
        M2C_FIELD(arg0, s32 *, 0xB4) = 0;
    }
    func_80203BC0_62EFA0(arg0, (u8)(M2C_FIELD(arg0, s32 *, 0xB4) + arg1));

    *(volatile s32 *)0x80000000 = 1;
}
