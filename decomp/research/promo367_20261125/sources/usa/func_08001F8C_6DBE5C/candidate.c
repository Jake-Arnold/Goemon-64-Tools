#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_8021C628_5D7AF8;
M2C_UNK func_08001FDC_6DBEAC();                     /* static */

void func_08001F8C_6DBE5C(void *arg0, M2C_UNK arg1) {
    if (!(M2C_FIELD(arg0, s32 *, 0x68) & 0x20)) {
        ((M2C_UNK(*)())&func_8021C628_5D7AF8)(arg0, 0x3F800000);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08001FDC_6DBEAC);
    }
}
