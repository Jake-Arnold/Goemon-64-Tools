#include "m2c_types.h"
void func_800388A0_394A0(u16, u8, s32);

void func_80038808_39408(u16 arg0) {
    func_800388A0_394A0(arg0, 0, 0);

    *(volatile s32 *)0x80000000 = 1;
}
