#include "m2c_types.h"
extern char func_80012030_12C30;
extern char func_800121B8_12DB8;
extern char func_80012490_13090;
extern char func_80023D48_24948;
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
extern char func_8003CF80_3DB80;
M2C_UNK func_080058A8_6D2528();                     /* static */
extern void *D_80201538_5BD508;

void func_080057D8_6D2458(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_80012030_12C30)(M2C_FIELD(arg0, s32 *, 0xE4), 0x41200000);
    ((M2C_UNK(*)())&func_800121B8_12DB8)(M2C_FIELD(arg0, s32 *, 0xE4), 0xC3A70000, 0x43A28000, 0x431D0000);
    ((M2C_UNK(*)())&func_80012490_13090)(M2C_FIELD(arg0, s32 *, 0xE4), M2C_FIELD(D_80201538_5BD508, s32 *, 0x2C) & 0x8FFFFFFE);
    if (((s32(*)())&func_80023D9C_2499C)(0x16A) != 0) {
        ((M2C_UNK(*)())&func_80023D48_24948)(0x16A);
        ((M2C_UNK(*)())&func_8003CF80_3DB80)(0x29E);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080058A8_6D2528);
    }
}
