#include "../m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_8021DB18_5D90A8;
extern char func_8021DFEC_5D957C;
M2C_UNK func_08003CD8_6BBA58();                     /* static */

void func_08003C7C_6BB9FC(s32 arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_8021DFEC_5D957C)();
    ((M2C_UNK(*)())&func_8021DB18_5D90A8)(arg0, 0x64, 0, 0);
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08003CD8_6BBA58);
}
