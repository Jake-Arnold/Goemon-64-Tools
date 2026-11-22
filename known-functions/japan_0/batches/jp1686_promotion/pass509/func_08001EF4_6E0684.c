#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_80221398_5DC928;
M2C_UNK func_08001F44_6E06D4();                     /* static */

void func_08001EF4_6E0684(void *arg0, M2C_UNK arg1) {
    if (!(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        ((M2C_UNK(*)())&func_80221398_5DC928)(arg0, 0x3F800000);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08001F44_6E06D4);
    }
}
