#include "m2c_types.h"
extern char func_80035020_35C20;
extern char func_8003521C_35E1C;
extern char func_802209F0_5DBEC0;
M2C_UNK func_08001374_6EFCD4();                     /* static */

void func_080012FC_6EFC5C(void *arg0, void *arg1) {
    s32 temp_v0;

    temp_v0 = ((s32(*)())&func_802209F0_5DBEC0)();
    M2C_FIELD(arg0, s32 *, 0xD8) = temp_v0;
    if (temp_v0 == 0) {
        ((M2C_UNK(*)())&func_80035020_35C20)();
        return;
    }
    M2C_FIELD(arg1, s32 *, 0x30) = (s32) (M2C_FIELD(arg0, s32 *, 0xD8) | 0x20000000);
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08001374_6EFCD4);
}
