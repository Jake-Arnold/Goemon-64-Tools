#include "m2c_types.h"
s32 func_801E4260_5A0170(s32, u8);
void func_801EB518_5A7428(s32, s32);
void func_801F5C4C_5B1B5C(s32, s32);

void func_801F5B9C_5B1AAC(s32 arg0, u8 arg1, s32 arg2) {
    if (func_801E4260_5A0170(arg0, arg1) != 0) {
        func_801EB518_5A7428(arg0, arg2);
    } else {
        func_801F5C4C_5B1B5C(arg0, arg2);
    }
}
