#include "m2c_types.h"
extern char func_80023CF8_248F8;
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
extern char func_801FF30C_5BB2DC;
extern char func_8021BB68_5D70F8;
M2C_UNK func_0800238C_6C654C();                     /* static */

void func_08002300_6C64C0(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_80023CF8_248F8)(0x15A);
    ((M2C_UNK(*)())&func_8021BB68_5D70F8)(arg0, 1);
    M2C_FIELD(arg0, s8 *, 0x6C) = 1;
    ((M2C_UNK(*)())&func_801FF30C_5BB2DC)(0xFF, 0xFF, 0xFF);
    ((M2C_UNK(*)())&func_80038808_39408)(0x2AD);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_0800238C_6C654C);
}
