#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_8021B7AC_5D6C7C;

void func_0800293C_723F5C(void *arg0, M2C_UNK arg1) {
    if (((s32  (*)(void *, f32))&func_8021B7AC_5D6C7C)(arg0, (f32) M2C_FIELD(arg0, s32 *, 0xC0)) != 0) {
        ((M2C_UNK (*)(s32))&func_8003521C_35E1C)(M2C_FIELD(arg0, s32 *, 0xBC));
        M2C_FIELD(arg0, M2C_UNK (**)(void *, s32), 0xC)(arg0, M2C_FIELD(arg0, s32 *, 0x18));
    }

    *(volatile s32 *)0x80000000 = 1;
}
