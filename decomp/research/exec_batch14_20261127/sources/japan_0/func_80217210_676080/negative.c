#include "m2c_types.h"

void func_800104B0_110B0(s32, s32, s32, s32, s32, s32, s32, s32);
extern s32 D_8021CBDC_67BA4C;
extern s32 D_8021CBE4_67BA54;

void func_80217210_676080(s32 arg0, s32 arg1, s32 arg2, s32 arg3) {
    s32 var_v0;
    s32 var_v1;

    switch (arg3) {
    case 1:
        var_v0 = D_8021CBDC_67BA4C;
        var_v1 = 0x18;
        break;
    case 2:
        var_v0 = D_8021CBE4_67BA54;
        var_v1 = 0;
        break;
    case 3:
        var_v0 = D_8021CBE4_67BA54;
        var_v1 = 0x18;
        break;
    default:
        return;
    }
    func_800104B0_110B0(arg0, arg1, arg2, 0x18, 0x18, var_v0, var_v1, 0);

    *(volatile int *)0x80000000 = 1;
}
