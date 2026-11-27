#include "m2c_types.h"

void func_800104B0_110B0(s32, s32, s32, s32, s32, s32, s32, s32);
extern s32 D_8021CBC8_67BA38;
extern s32 D_8021CBCC_67BA3C;

void func_8021730C_67617C(s32 arg0, s32 arg1, s32 arg2, s32 arg3) {
    s32 var_v0;
    s32 var_v1;

    switch (arg3) {
    case 0:
        var_v0 = D_8021CBC8_67BA38;
        var_v1 = 0;
        break;
    case 1:
        var_v0 = D_8021CBC8_67BA38;
        var_v1 = 0x18;
        break;
    case 2:
        var_v0 = D_8021CBCC_67BA3C;
        var_v1 = 0;
        break;
    default:
        return;
    }
    func_800104B0_110B0(arg0, arg1, arg2, 0x18, 0x18, var_v0, var_v1, 0);
}
