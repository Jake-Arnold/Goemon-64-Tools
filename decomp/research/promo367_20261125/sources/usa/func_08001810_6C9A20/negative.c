#include "m2c_types.h"
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern char func_80218DCC_5D429C;
M2C_UNK func_080018B4_6C9AC4();                     /* static */
extern M2C_UNK D_8015CC30_15D830;

void func_08001810_6C9A20(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (((s32(*)())&func_800240DC_24CDC)(0x16C) == 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 0x01000000);
        if (M2C_FIELD(&D_8015CC30_15D830, s32 *, 0x184) & 8) {
            M2C_FIELD(&D_8015CC30_15D830, s32 *, 0x184) = (s32) (M2C_FIELD(&D_8015CC30_15D830, s32 *, 0x184) | 0x40);
        }
        ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 8, 0x3E800000, 4);
        ((M2C_UNK(*)())&func_80218DCC_5D429C)(arg0, 9);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080018B4_6C9AC4);
    }
}
