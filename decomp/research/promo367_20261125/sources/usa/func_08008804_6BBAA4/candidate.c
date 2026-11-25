#include "m2c_types.h"
extern char func_80012628_13228;
extern char func_80012900_13500;
extern char func_8003521C_35E1C;
M2C_UNK func_08008888_6BBB28();                     /* static */
extern void *D_801FC628_5B8538;

void func_08008804_6BBAA4(void *arg0, M2C_UNK arg1) {
    s32 sp1C;

    sp1C = M2C_FIELD(D_801FC628_5B8538, s32 *, 0x2C) & 0x8FFFFFFE;
    ((M2C_UNK(*)())&func_80012628_13228)(M2C_FIELD(arg0, s32 *, 0xD0), 0x42D20000, 0xC1F00000, 0x42B40000);
    ((M2C_UNK(*)())&func_80012900_13500)(M2C_FIELD(arg0, s32 *, 0xD0), sp1C);
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08008888_6BBB28);
}
