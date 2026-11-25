#include "m2c_types.h"
extern char func_80023E94_24A94;
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
M2C_UNK func_08004FDC_6C472C();                     /* static */
extern f32 D_08008A44_6C8194;

void func_08004F74_6C46C4(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80023E94_24A94)(0) != 0) {
        M2C_FIELD(arg0, f32 *, 0x7C) = (f32) D_08008A44_6C8194;
        ((M2C_UNK(*)())&func_80038B98_39798)(0x2AD);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08004FDC_6C472C);
    }
}
