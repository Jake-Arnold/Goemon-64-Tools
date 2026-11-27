#include "m2c_types.h"

void func_800104B0_110B0(s32, s32, s32, s32, s32, s32, s32, s32);
extern s32 D_8021CBD0_67BA40;
extern s32 D_8021CBE8_67BA58;

void func_80217190_676000(s32 arg0, s32 arg1, s32 arg2, s32 arg3) {
    s32 var_v0;
    s32 var_v1;

    switch (arg3) {
    case 1:
        var_v0 = D_8021CBD0_67BA40;
        var_v1 = 0x18;
        break;
    case 2:
        var_v0 = D_8021CBE8_67BA58;
        var_v1 = 0;
        break;
    case 3:
        var_v0 = D_8021CBE8_67BA58;
        var_v1 = 0x18;
        break;
    default:
        return;
    }
    func_800104B0_110B0(arg0, arg1, arg2, 0x18, 0x18, var_v0, var_v1, 0);
}
