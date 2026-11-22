#include "m2c_types.h"
extern char func_80023AB0_246B0;
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
M2C_UNK func_08002A20_6C6BE0();                     /* static */
extern void *D_80201514_5BD4E4;
extern M2C_UNK g_system;

void func_080029A0_6C6B60(void *arg0, s32 arg1) {
    ((M2C_UNK(*)())&func_80023AB0_246B0)(0);
    if (arg1 != M2C_FIELD(D_80201514_5BD4E4, s32 *, 0xA0)) {
        ((M2C_UNK(*)())&func_80038808_39408)(0x155);
        M2C_FIELD(&g_system, s8 *, 0xCF8A2) = 0;
        M2C_FIELD(arg0, s16 *, 0x8A) = 0xA;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08002A20_6C6BE0);
    }
}
