#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_801FB240_5B7150;
extern char func_80221EBC_5DD38C;
extern char func_80221F70_5DD440;
M2C_UNK func_080012C8_6F47A8();                     /* static */
extern M2C_UNK D_8015CC30_15D830;

void func_08001240_6F4720(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_80221F70_5DD440)();
    ((M2C_UNK(*)())&func_80221EBC_5DD38C)();
    M2C_FIELD(&D_8015CC30_15D830, s32 *, 0xD4) = (s32) (M2C_FIELD(&D_8015CC30_15D830, s32 *, 0xD4) | 1);
    if (M2C_FIELD(arg0, s32 *, 0xEC) & 2) {
        ((M2C_UNK(*)())&func_801FB240_5B7150)();
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080012C8_6F47A8);
    }
}
