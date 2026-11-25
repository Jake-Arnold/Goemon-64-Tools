#include "m2c_types.h"
extern char func_8021664C_5D1B1C;
extern char func_80218D7C_5D424C;
extern char func_80218DA8_5D4278;
extern char func_8021927C_5D474C;
extern char func_80219E70_5D5340;
extern char func_8021A644_5D5B14;
extern char func_8021B064_5D6534;
extern char func_8021B09C_5D656C;
extern char func_80224ABC_5DFF8C;
M2C_UNK func_08000554_6E7864();                     /* static */
extern M2C_UNK D_08001C90_6E8FA0;

void func_08000000_6E7310(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_8021A644_5D5B14)();
    M2C_FIELD(arg0, s32 *, 0x60) = 0x2006E3;
    ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 0, 0x3E800000, 1);
    ((M2C_UNK(*)())&func_80224ABC_5DFF8C)(arg0, 0, 0x3F800000, 1);
    M2C_FIELD(arg0, s8 *, 0x8D) = 0x10;
    M2C_FIELD(arg0, M2C_UNK (**)(), 0x90) = func_08000554_6E7864;
    ((M2C_UNK(*)())&func_80218D7C_5D424C)(arg0, 0x32, 0x64, 0);
    ((M2C_UNK(*)())&func_80218DA8_5D4278)(arg0, 0x190, 0x28, 0);
    ((M2C_UNK(*)())&func_8021927C_5D474C)(arg0);
    ((M2C_UNK(*)())&func_80219E70_5D5340)(arg0, 5, 0);
    ((M2C_UNK(*)())&func_8021B064_5D6534)(arg0, &D_08001C90_6E8FA0, 0);
    ((M2C_UNK(*)())&func_8021B09C_5D656C)(arg0, 0, 1);
}
