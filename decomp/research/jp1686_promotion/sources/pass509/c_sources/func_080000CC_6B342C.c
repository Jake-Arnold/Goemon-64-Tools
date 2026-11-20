#include "m2c_types.h"
extern char func_80023CF8_248F8;
extern char func_80034E8C_35A8C;
extern char func_8003CF80_3DB80;
extern char func_8021DB18_5D90A8;
extern char func_8021EF9C_5DA52C;
M2C_UNK func_08000164_6B34C4();                     /* static */

void func_080000CC_6B342C(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, s32 *, 0x68) & 0x200) {
        ((M2C_UNK(*)())&func_8003CF80_3DB80)(0x6C);
        ((M2C_UNK(*)())&func_8021DB18_5D90A8)(arg0, 0, 0, 0);
        ((M2C_UNK(*)())&func_8021EF9C_5DA52C)(arg0);
        ((M2C_UNK(*)())&func_80023CF8_248F8)(M2C_FIELD(arg0, u16 *, 0xD0));
        M2C_FIELD(arg0, s32 *, 0x60) = 0;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08000164_6B34C4);
    }
}
