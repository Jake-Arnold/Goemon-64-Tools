#include "m2c_types.h"
M2C_UNK func_8003521C_35E1C(s32);
extern void *D_801FC604_5B8514;

void func_08001158_7117B8(void *arg0, u16 arg1) {
    M2C_UNK (*fn)(s32) = func_8003521C_35E1C;
    if (M2C_FIELD(D_801FC604_5B8514, u16 *, 0x98) != 0) {
        fn(M2C_FIELD(arg0, s32 *, 0xBC));
        M2C_FIELD(arg0, M2C_UNK (**)(void *, s32), 0xC)(arg0, M2C_FIELD(arg0, s32 *, 0x18));
    }
}
