#include "m2c_types.h"
extern char func_8021664C_5D1B1C;
extern char func_80218D90_5D4260;
extern char func_80219E70_5D5340;
extern char func_8021A644_5D5B14;
extern char func_8021B064_5D6534;
extern char func_8021B09C_5D656C;
extern M2C_UNK D_08003DC0_6D9D10;

void func_080011F0_6D7140(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    ((M2C_UNK(*)())&func_8021A644_5D5B14)();
    M2C_FIELD(arg0, s32 *, 0x60) = 0x02248361;
    M2C_FIELD(arg0, s8 *, 0x8E) = 1;
    M2C_FIELD(arg0, s8 *, 0x8F) = 2;
    M2C_FIELD(arg0, s16 *, 0x96) = 0x1E1;
    M2C_FIELD(arg0, s16 *, 0x4E) = 0x14;
    ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 0, 0x3EAAAAAB, 1);
    ((M2C_UNK(*)())&func_80219E70_5D5340)(arg0, 0xA, 0);
    ((M2C_UNK(*)())&func_80218D90_5D4260)(arg0, 0x28, 0x14, 0x14, -0x14);
    ((M2C_UNK(*)())&func_8021B064_5D6534)(arg0, &D_08003DC0_6D9D10, 0);
    ((M2C_UNK(*)())&func_8021B09C_5D656C)(arg0, 0, 1);
}
