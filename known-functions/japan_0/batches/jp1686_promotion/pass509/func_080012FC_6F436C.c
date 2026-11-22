#include "m2c_types.h"
extern char func_80034C90_35890;
extern char func_80034E8C_35A8C;
extern char func_80225760_5E0CF0;
M2C_UNK func_08001374_6F43E4();                     /* static */

void func_080012FC_6F436C(void *arg0, void *arg1) {
    s32 temp_v0;

    temp_v0 = ((s32(*)())&func_80225760_5E0CF0)();
    M2C_FIELD(arg0, s32 *, 0xD8) = temp_v0;
    if (temp_v0 == 0) {
        ((M2C_UNK(*)())&func_80034C90_35890)();
        return;
    }
    M2C_FIELD(arg1, s32 *, 0x30) = (s32) (M2C_FIELD(arg0, s32 *, 0xD8) | 0x20000000);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08001374_6F43E4);
}
