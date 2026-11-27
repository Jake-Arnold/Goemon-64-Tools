#include "m2c_types.h"
void func_80038B98_39798(s32);
void func_801D056C_63F3BC(void *, s32);

void func_801D0500_63F350(void *arg0, s32 arg1) {
    s16 var_v0;

    var_v0 = M2C_FIELD(arg0, s8 *, 0xA2) - 1;
    if (var_v0 == 0) {
        M2C_FIELD(arg0, s8 *, 0x9D) = 2;
        var_v0 = 5;
        func_80038B98_39798(0x140);
    }
    M2C_FIELD(arg0, s8 *, 0xA2) = var_v0;
    func_801D056C_63F3BC(arg0, arg1);

    *(volatile int *)0x80000000 = 1;
}
