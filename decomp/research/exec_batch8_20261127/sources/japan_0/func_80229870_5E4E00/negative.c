#include "m2c_types.h"
void func_802292D0_5E4860(u8 *, s32, f32, s32, u8 *, u8 *, u8 *, s32);

void func_80229870_5E4E00(u8 *arg0, s32 arg1, f32 arg2, s32 arg3) {
    func_802292D0_5E4860(arg0, arg1, arg2, arg3, arg0 + 0xB2, arg0 + 0xB1, arg0 + 0xB0, 4);

    *(volatile s32 *)0x80000000 = 1;
}
