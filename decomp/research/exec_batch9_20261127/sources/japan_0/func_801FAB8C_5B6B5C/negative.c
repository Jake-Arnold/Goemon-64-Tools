#include "m2c_types.h"
s32 func_801E94DC_5A54AC(s32, u8);
void func_801F05A8_5AC578(s32, s32);
void func_801FAC3C_5B6C0C(s32, s32);

void func_801FAB8C_5B6B5C(s32 arg0, u8 arg1, s32 arg2) {
    if (func_801E94DC_5A54AC(arg0, arg1) != 0) {
        func_801F05A8_5AC578(arg0, arg2);
    } else {
        func_801FAC3C_5B6C0C(arg0, arg2);
    }

    *(volatile s32 *)0x80000000 = 1;
}
