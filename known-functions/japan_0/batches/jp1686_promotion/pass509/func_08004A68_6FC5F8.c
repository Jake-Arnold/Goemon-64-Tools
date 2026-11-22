#include "m2c_types.h"
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
extern char func_80200150_5BC120;
extern char func_80224FDC_5E056C;
M2C_UNK func_08004B08_6FC698();                     /* static */
extern M2C_UNK D_80162420_163020;
extern M2C_UNK g_system;

void func_08004A68_6FC5F8(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, u16 *, 0xDA) != 0) {
        M2C_FIELD(&D_80162420_163020, s32 *, 0xD4) = (s32) (M2C_FIELD(&D_80162420_163020, s32 *, 0xD4) | 1);
        ((M2C_UNK(*)())&func_80038808_39408)(0x108);
        ((M2C_UNK(*)())&func_80200150_5BC120)();
        M2C_FIELD(&g_system, s8 *, 0xCF8A2) = 1;
        ((M2C_UNK(*)())&func_80224FDC_5E056C)(arg0, 0xFF, 0xFF, 0xFF);
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08004B08_6FC698);
    }
}
