#include "m2c_types.h"
extern char func_80024038_24C38;
extern char func_8003521C_35E1C;
extern s8 D_8015CDB4;
extern M2C_UNK func_08003058_6B62F8;

void func_08002FFC_6B629C(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    ((M2C_UNK(*)())&func_80024038_24C38)(0x179);
    M2C_FIELD(arg0, s32 *, 0xE8) = (s32) (M2C_FIELD(arg0, s32 *, 0xE8) | 0x400);
    D_8015CDB4 = 0;
    ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08003058_6B62F8);
}
