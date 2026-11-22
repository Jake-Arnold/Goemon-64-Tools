#include "m2c_types.h"
extern char func_80023CF8_248F8;
extern char func_801FF3B4_5BB384;
extern char func_80225FCC_5E155C;

void func_08003CD8_6BBA58(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_80225FCC_5E155C)();
    if (M2C_FIELD(arg0, s32 *, 0x68) & 0x4000) {
        ((M2C_UNK(*)())&func_80023CF8_248F8)(0x97);
        ((M2C_UNK(*)())&func_801FF3B4_5BB384)(0x28, -0x6E, -0x46, 0x27, 0x100);
    }
}
