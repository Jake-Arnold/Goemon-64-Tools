#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_8021C628_5D7AF8;
M2C_UNK func_08002EF4_6D1FD4();                     /* static */

void func_08002EA4_6D1F84(void *arg0, M2C_UNK arg1) {
    if (!(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        ((M2C_UNK(*)())&func_8021C628_5D7AF8)(arg0, 0x40000000);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08002EF4_6D1FD4);
    }
}
