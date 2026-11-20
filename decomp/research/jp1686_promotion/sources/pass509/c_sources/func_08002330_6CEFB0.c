#include "m2c_types.h"
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
extern char func_8021B3BC_5D694C;
extern char func_8021DB3C_5D90CC;
M2C_UNK func_080023C0_6CF040();                     /* static */

void func_08002330_6CEFB0(void *arg0, void *arg1) {
    if ((((s32(*)())&func_80023D9C_2499C)(0x16C) == 0) && (M2C_FIELD(arg1, u8 *, 0x7C) & 2)) {
        ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 2, 0x3E800000, 4);
        ((M2C_UNK(*)())&func_8021DB3C_5D90CC)(arg0, 3);
        M2C_FIELD(arg0, s16 *, 0x8A) = 0;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080023C0_6CF040);
    }
}
