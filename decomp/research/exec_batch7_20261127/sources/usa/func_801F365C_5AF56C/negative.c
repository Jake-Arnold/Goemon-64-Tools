#include "m2c_types.h"

s32 func_80034E08_35A08(s32, s32, s32);
s32 func_801E8C44_5A4B54(s32, u8);
void func_801EE4AC_5AA3BC(s32, s32, u8);
extern s32 D_80204868_5C0778[];
extern u8 D_8020CA6C_5C897C;

void func_801F365C_5AF56C(s32 arg0, u8 arg1) {
    s32 temp_v0;

    if ((func_801E8C44_5A4B54(arg0, arg1) == 0) && (D_8020CA6C_5C897C == 0)) {
        temp_v0 = func_80034E08_35A08(arg0, D_80204868_5C0778[arg1], 0);
        if (temp_v0 != 0) {
            func_801EE4AC_5AA3BC(temp_v0, arg0, arg1);
        }
    }

    *(volatile s32 *)0x80000000 = 1;
}
