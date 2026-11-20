#include "../m2c_types.h"
extern char func_8021DFEC_5D957C;
extern char func_8021FE0C_5DB39C;

void func_08000504_6EBF34(s32 arg0, void *arg1) {
    M2C_FIELD(arg1, u16 *, 0x16) = (u16) (M2C_FIELD(arg1, u16 *, 0x16) + 2);
    ((M2C_UNK(*)())&func_8021DFEC_5D957C)(arg0);
    ((M2C_UNK(*)())&func_8021FE0C_5DB39C)(arg0, 1, 0);
}
