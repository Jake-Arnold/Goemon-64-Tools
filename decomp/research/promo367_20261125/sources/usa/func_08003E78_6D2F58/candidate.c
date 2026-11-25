#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern char func_8021A644_5D5B14;
extern char func_80224ABC_5DFF8C;
M2C_UNK func_08003F70_6D3050();                     /* static */
M2C_UNK func_080040D8_6D31B8();                     /* static */

void func_08003E78_6D2F58(s32 arg0, M2C_UNK arg1) {
    s32 temp_v0;

    ((M2C_UNK(*)())&func_8021A644_5D5B14)();
    ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 0, 0x3F800000, 0);
    M2C_FIELD(arg0, s16 *, 0x8A) = (s16) (((u32) ((arg0 & 0x3FF) * 0x12C) >> 0xA) + 2);
    ((M2C_UNK(*)())&func_80224ABC_5DFF8C)(arg0, 0, 0x3F800000, 0);
    temp_v0 = M2C_FIELD(arg0, s32 *, 0xD0);
    switch (temp_v0) {                              /* irregular */
    case 0:
        M2C_FIELD(arg0, s32 *, 0x60) = 0x2A0CE3;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08003F70_6D3050);
        return;
    case 1:
        M2C_FIELD(arg0, s32 *, 0x60) = 0x2A0EE3;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080040D8_6D31B8);
        return;
    }
}
