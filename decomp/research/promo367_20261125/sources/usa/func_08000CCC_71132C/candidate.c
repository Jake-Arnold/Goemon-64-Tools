#include "m2c_types.h"
extern char func_8021664C_5D1B1C;
extern char func_80220F70_5DC440;

void func_08000CCC_71132C(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;

    ((M2C_UNK(*)())&func_80220F70_5DC440)();
    temp_v0 = M2C_FIELD(arg0, s32 *, 0x68);
    if (temp_v0 & 0x4000) {
        M2C_FIELD(arg0, s32 *, 0x68) = (s32) (temp_v0 & ~0x4000);
        ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 0, 0x3E800000, 1);
    }
}
