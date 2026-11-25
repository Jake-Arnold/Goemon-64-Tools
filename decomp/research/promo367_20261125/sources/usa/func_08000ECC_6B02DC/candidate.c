#include "m2c_types.h"
extern char func_80023E94_24A94;
extern char func_802213F4_5DC8C4;

void func_08000ECC_6B02DC(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_802213F4_5DC8C4)();
    if (((s32(*)())&func_80023E94_24A94)(2) == 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & 0xEFFFFFFF);
    }
}
