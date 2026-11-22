#include "m2c_types.h"
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
extern char func_8021B3BC_5D694C;
extern char func_8021DB3C_5D90CC;
M2C_UNK func_08001864_6CE4E4();                     /* static */
extern M2C_UNK D_80162420_163020;

void func_080017C0_6CE440(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80023D9C_2499C)(0x16C) == 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 0x01000000);
        if (M2C_FIELD(&D_80162420_163020, s32 *, 0x184) & 8) {
            M2C_FIELD(&D_80162420_163020, s32 *, 0x184) = (s32) (M2C_FIELD(&D_80162420_163020, s32 *, 0x184) | 0x40);
        }
        ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 8, 0x3E800000, 4);
        ((M2C_UNK(*)())&func_8021DB3C_5D90CC)(arg0, 9);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08001864_6CE4E4);
    }
}
