#include "m2c_types.h"

void func_800106F0_112F0(s32, s32, s32, s32, s32, s32, s32, s32);
extern s32 D_80217F9C_676F4C;
extern s32 D_80217FA4_676F54;

void func_802123F0_6713A0(s32 arg0, s32 arg1, s32 arg2, s32 arg3) {
    s32 var_v0;
    s32 var_v1;

    switch (arg3) {
    case 1:
        var_v0 = D_80217F9C_676F4C;
        var_v1 = 0x18;
        break;
    case 2:
        var_v0 = D_80217FA4_676F54;
        var_v1 = 0;
        break;
    case 3:
        var_v0 = D_80217FA4_676F54;
        var_v1 = 0x18;
        break;
    default:
        return;
    }
    func_800106F0_112F0(arg0, arg1, arg2, 0x18, 0x18, var_v0, var_v1, 0);
}
