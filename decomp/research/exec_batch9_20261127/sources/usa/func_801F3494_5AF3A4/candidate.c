#include "m2c_types.h"

void *func_80034E08_35A08(s32, s32, s32);
s32 func_801E8C44_5A4B54(s32, u8);
void func_801EE4AC_5AA3BC(void *, s32, u8);
extern s32 D_80204868_5C0778[];
extern u8 D_8020CA6C_5C897C;

void func_801F3494_5AF3A4(s32 arg0, u8 arg1) {
    void *temp_v0;

    if ((func_801E8C44_5A4B54(arg0, arg1) == 0) && (D_8020CA6C_5C897C == 0)) {
        temp_v0 = func_80034E08_35A08(arg0, D_80204868_5C0778[arg1], 0);
        if (temp_v0 != NULL) {
            func_801EE4AC_5AA3BC(temp_v0, arg0, arg1);
            M2C_FIELD(temp_v0, s16 *, 0x68) = 1;
        }
    }
}
