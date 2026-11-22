#include "m2c_types.h"
extern s32 D_80072C38_73838;
extern s32 D_80072C3C_7383C;
extern s32 D_80072C40_73840;
extern s32 D_80072C44_73844;

s32 func_80021380_21F80(s32 arg0, s32 arg1, s32 arg2, s32 arg3) {
    if (arg0 < 0) {
        return 0;
    }
    if (arg2 >= 0x141) {
        return 0;
    }
    if (arg1 < 0) {
        return 0;
    }
    if (arg3 >= 0xF1) {
        return 0;
    }
    if (arg2 < arg0) {
        return 0;
    }
    if (arg3 < arg1) {
        return 0;
    }
    D_80072C38_73838 = arg0;
    D_80072C3C_7383C = arg1;
    D_80072C40_73840 = arg2;
    D_80072C44_73844 = arg3;
    return 1;
}
