#include "m2c_types.h"
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
M2C_UNK func_08000AB0_6C8CC0();                     /* static */

void func_08000A0C_6C8C1C(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    if (((s32(*)())&func_800240DC_24CDC)(0x16C) == 0) {
        if (M2C_FIELD(arg1, u8 *, 0x7C) & 4) {
            M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (M2C_FIELD(arg0, u16 *, 0x8A) + 1);
        }
        if (M2C_FIELD(arg0, u16 *, 0x8A) == 2) {
            M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 0x01000000);
            ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 0, 0x3E800000, 4);
            ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08000AB0_6C8CC0);
        }
    }
}
