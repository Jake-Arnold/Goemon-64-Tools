#include "../m2c_types.h"
extern char func_80012F90_13B90;
extern char func_80034B68_35768;

s32 func_08000920_7407F0(void *arg0) {
    ((M2C_UNK(*)())&func_80012F90_13B90)(M2C_FIELD(arg0, s32 *, 0x68), M2C_FIELD(arg0, u8 *, 0x6C), M2C_FIELD(arg0, u8 *, 0x6D), M2C_FIELD(arg0, u8 *, 0x6E));
    ((M2C_UNK(*)())&func_80034B68_35768)(arg0);
    return 0;
}
