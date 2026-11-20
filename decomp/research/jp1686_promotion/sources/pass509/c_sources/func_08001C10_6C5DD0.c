#include "m2c_types.h"
extern char func_80023CF8_248F8;
extern char func_80034E8C_35A8C;
extern char func_8003CF80_3DB80;
extern char func_8021CDBC_5D834C;
extern char func_8021DB18_5D90A8;
extern char func_8021EF9C_5DA52C;
extern char func_80226CE0_5E2270;
M2C_UNK func_08001CCC_6C5E8C();                     /* static */

void func_08001C10_6C5DD0(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, s32 *, 0x68) & 0x200) {
        ((M2C_UNK(*)())&func_80226CE0_5E2270)();
        ((M2C_UNK(*)())&func_8003CF80_3DB80)(0x83);
        ((M2C_UNK(*)())&func_80023CF8_248F8)(0x1A3);
        ((M2C_UNK(*)())&func_8021DB18_5D90A8)(arg0, 0, 0, 0);
        ((M2C_UNK(*)())&func_8021EF9C_5DA52C)(arg0);
        M2C_FIELD(arg0, s32 *, 0x60) = 0;
        ((M2C_UNK(*)())&func_8021CDBC_5D834C)(arg0, 0);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08001CCC_6C5E8C);
    }
}
