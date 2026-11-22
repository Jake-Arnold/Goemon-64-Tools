#include "m2c_types.h"
extern char func_8021DFEC_5D957C;
extern char func_8021E548_5D9AD8;
extern char func_8021FE0C_5DB39C;

void func_08002F3C_6D6A3C(s32 arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_8021E548_5D9AD8)(arg0, 8) == 0) {
        ((M2C_UNK(*)())&func_8021DFEC_5D957C)(arg0);
        ((M2C_UNK(*)())&func_8021FE0C_5DB39C)(arg0, 0, 1);
    }
}
