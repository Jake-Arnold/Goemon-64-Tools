#include "m2c_types.h"

void func_80003728_4328(s32);
void func_8000607C_6C7C(u16, s16, s16, s16, u16, u16, u16, s32);
extern s16 D_800C7AD6_C86D6;

void func_80005FFC_6BFC(u16 arg0, s16 arg1, s16 arg2, s16 arg3, u16 arg4, u16 arg5, u16 arg6, s32 arg7) {
    func_8000607C_6C7C(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7);
    D_800C7AD6_C86D6 = 2;
    func_80003728_4328(0x10);
}
