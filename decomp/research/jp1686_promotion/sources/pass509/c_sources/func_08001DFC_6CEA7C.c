#include "m2c_types.h"
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
extern char func_8021B3BC_5D694C;
extern char func_8021DB3C_5D90CC;
extern char func_8021E46C_5D99FC;
M2C_UNK func_08001EB8_6CEB38();                     /* static */

void func_08001DFC_6CEA7C(void *arg0, void *arg1) {
    if ((((s32(*)())&func_80023D9C_2499C)(0x16C) == 0) && (((s32(*)())&func_8021E46C_5D99FC)(arg0, M2C_FIELD(arg0, s32 *, 0xE0), M2C_FIELD(arg1, s32 *, 0xC), M2C_FIELD(arg0, s32 *, 0xE4), 0x10) == 0)) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 0x01000000);
        ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 0x10, 0x3F000000, 4);
        ((M2C_UNK(*)())&func_8021DB3C_5D90CC)(arg0, 0x11);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08001EB8_6CEB38);
    }
}
