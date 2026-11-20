#include "m2c_types.h"
extern char func_80034C90_35890;
extern char func_80034E8C_35A8C;
extern char func_80225760_5E0CF0;
M2C_UNK func_0800121C_6F428C();                     /* static */

void func_080011A0_6F4210(void *arg0, void *arg1) {
    s32 temp_v0;

    M2C_FIELD(arg0, s16 *, 0xD4) = 0;
    temp_v0 = ((s32(*)())&func_80225760_5E0CF0)();
    M2C_FIELD(arg0, s32 *, 0xD8) = temp_v0;
    if (temp_v0 == 0) {
        ((M2C_UNK(*)())&func_80034C90_35890)();
        return;
    }
    M2C_FIELD(arg1, s32 *, 0x30) = (s32) (M2C_FIELD(arg0, s32 *, 0xD8) | 0x20000000);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_0800121C_6F428C);
}
