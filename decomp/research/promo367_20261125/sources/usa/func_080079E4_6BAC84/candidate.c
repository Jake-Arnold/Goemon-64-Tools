#include "../m2c_types.h"
extern char func_80023DF0_249F0;
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
extern char func_80218D7C_5D424C;
M2C_UNK func_08007A64_6BAD04();                     /* static */

void func_080079E4_6BAC84(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_80038B98_39798)(0x8243);
    M2C_FIELD(arg0, s32 *, 0xE8) = (s32) (M2C_FIELD(arg0, s32 *, 0xE8) | 0x80);
    ((M2C_UNK(*)())&func_80023DF0_249F0)(8);
    ((M2C_UNK(*)())&func_80218D7C_5D424C)(arg0, 0, 0, 0);
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08007A64_6BAD04);
}
