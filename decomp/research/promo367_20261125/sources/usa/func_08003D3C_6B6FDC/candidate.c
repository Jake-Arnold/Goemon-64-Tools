#include "m2c_types.h"
extern char func_80024038_24C38;
extern char func_801FA4A4_5B63B4;
extern char func_8022125C_5DC72C;

void func_08003D3C_6B6FDC(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_8022125C_5DC72C)();
    if (M2C_FIELD(arg0, s32 *, 0x68) & 0x4000) {
        ((M2C_UNK(*)())&func_80024038_24C38)(0x97);
        ((M2C_UNK(*)())&func_801FA4A4_5B63B4)(0x28, -0x6E, -0x46, 0x27, 0x100);
    }
}
