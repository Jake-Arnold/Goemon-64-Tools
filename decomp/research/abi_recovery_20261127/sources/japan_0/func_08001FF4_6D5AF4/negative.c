#include "m2c_types.h"
extern char func_8022B618_5E6BA8;

void func_08001FF4_6D5AF4(void *arg0, M2C_UNK arg1) {
    if (((s32  (*)(void *))&func_8022B618_5E6BA8)(arg0) != 0) {
        M2C_FIELD(arg0, s32 *, 0x68) = (s32) (M2C_FIELD(arg0, s32 *, 0x68) | 2);
    }

    *(volatile s32 *)0x80000000 = 1;
}
