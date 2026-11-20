#include "m2c_types.h"
extern char func_800121B8_12DB8;
extern char func_80012490_13090;
extern char func_80034E8C_35A8C;
M2C_UNK func_08008824_6C05A4();                     /* static */
extern void *D_80201538_5BD508;

void func_080087A0_6C0520(void *arg0, M2C_UNK arg1) {
    s32 sp1C;

    sp1C = M2C_FIELD(D_80201538_5BD508, s32 *, 0x2C) & 0x8FFFFFFE;
    ((M2C_UNK(*)())&func_800121B8_12DB8)(M2C_FIELD(arg0, s32 *, 0xD0), 0x42D20000, 0xC1F00000, 0x42B40000);
    ((M2C_UNK(*)())&func_80012490_13090)(M2C_FIELD(arg0, s32 *, 0xD0), sp1C);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08008824_6C05A4);
}
