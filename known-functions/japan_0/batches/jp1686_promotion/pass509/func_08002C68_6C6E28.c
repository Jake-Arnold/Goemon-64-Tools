#include "m2c_types.h"
extern char func_80023AB0_246B0;
extern char func_80034E8C_35A8C;
extern char func_80038808_39408;
M2C_UNK func_08002CEC_6C6EAC();                     /* static */
extern void *D_80201514_5BD4E4;
extern M2C_UNK g_system;

void func_08002C68_6C6E28(void *arg0, s32 arg1) {
    ((M2C_UNK(*)())&func_80023AB0_246B0)(1);
    if (arg1 != M2C_FIELD(D_80201514_5BD4E4, s32 *, 0xA0)) {
        ((M2C_UNK(*)())&func_80038808_39408)(0x155);
        M2C_FIELD(&g_system, s8 *, 0xCF8A2) = 1;
        M2C_FIELD(arg0, s16 *, 0x8A) = 0xA;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08002CEC_6C6EAC);
    }
}
