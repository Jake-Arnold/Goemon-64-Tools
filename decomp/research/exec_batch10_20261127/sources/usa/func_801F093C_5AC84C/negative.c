#include "m2c_types.h"
void *func_80034E08_35A08(void *, s32, s32);
s32 func_80035EEC_36AEC(void *, s32, s32);
M2C_UNK func_801EE4AC_5AA3BC(void *, void *, u8);
extern s32 D_80204868_5C0778[];

void func_801F093C_5AC84C(void *arg0, u8 arg1) {
    void *temp_v0;

    temp_v0 = func_80034E08_35A08(arg0, D_80204868_5C0778[arg1], 0);
    if (temp_v0 != NULL) {
        func_801EE4AC_5AA3BC(temp_v0, arg0, arg1);
        if (func_80035EEC_36AEC(temp_v0, 2, 3) == 0) {
            M2C_FIELD(temp_v0, s8 *, 0x65) = 1;
        }
    }

    *(volatile s32 *)0x80000000 = 1;
}
