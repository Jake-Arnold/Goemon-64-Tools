#include "m2c_types.h"
extern char func_80225CE0_5E1270;
extern char func_80229AC0_5E5050;
extern char func_8022B618_5E6BA8;

void func_08000464_7203B4(s32 arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80225CE0_5E1270)() == 0) {
        ((M2C_UNK(*)())&func_80229AC0_5E5050)(arg0, 2);
        ((M2C_UNK(*)())&func_8022B618_5E6BA8)(arg0);
    }
}
