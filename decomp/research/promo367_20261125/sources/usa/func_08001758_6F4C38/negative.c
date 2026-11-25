#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern u16 D_8015CC30_15D830;
extern M2C_UNK func_080017EC_6F4CCC;

void func_08001758_6F4C38(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_v0;

    if (((s32) D_8015CC30_15D830 % 4) < 2) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & ~0x20);
    } else {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 0x20);
    }
    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        M2C_FIELD(arg0, u16 *, 0x8A) = 0xFU;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_080017EC_6F4CCC, arg0);
    }
}
