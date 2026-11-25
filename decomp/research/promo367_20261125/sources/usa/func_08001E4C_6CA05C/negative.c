#include "m2c_types.h"
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern char func_80218DCC_5D429C;
extern char func_802196FC_5D4BCC;
M2C_UNK func_08001F08_6CA118();                     /* static */

void func_08001E4C_6CA05C(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    if ((((s32(*)())&func_800240DC_24CDC)(0x16C) == 0) && (((s32(*)())&func_802196FC_5D4BCC)(arg0, M2C_FIELD(arg0, s32 *, 0xE0), M2C_FIELD(arg1, s32 *, 0xC), M2C_FIELD(arg0, s32 *, 0xE4), 0x10) == 0)) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 0x01000000);
        ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 0x10, 0x3F000000, 4);
        ((M2C_UNK(*)())&func_80218DCC_5D429C)(arg0, 0x11);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08001F08_6CA118);
    }
}
