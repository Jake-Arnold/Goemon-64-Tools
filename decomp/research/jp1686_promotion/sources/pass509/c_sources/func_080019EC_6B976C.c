#include "m2c_types.h"
extern char func_80023CF8_248F8;
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
M2C_UNK func_08001A44_6B97C4();                     /* static */

void func_080019EC_6B976C(s32 arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80023D9C_2499C)(0x175) != 0) {
        ((M2C_UNK(*)())&func_80023CF8_248F8)(0x178);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08001A44_6B97C4);
    }
}
