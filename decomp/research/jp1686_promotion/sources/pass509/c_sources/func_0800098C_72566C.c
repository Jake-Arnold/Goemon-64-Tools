#include "m2c_types.h"
extern char func_80023CF8_248F8;
extern char func_80023D9C_2499C;
extern char func_80034B44_35744;
extern char func_8003CF80_3DB80;

void func_0800098C_72566C(s32 arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80023D9C_2499C)(0x199) == 0) {
        ((M2C_UNK(*)())&func_80023CF8_248F8)(0x199);
        ((M2C_UNK(*)())&func_8003CF80_3DB80)(0x137);
    }
    ((M2C_UNK(*)())&func_80034B44_35744)();
}
