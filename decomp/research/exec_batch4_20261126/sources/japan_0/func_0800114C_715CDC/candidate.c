#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(s32);
extern void *D_80201514_5BD4E4;

void func_0800114C_715CDC(void *arg0, u16 arg1) {
    M2C_UNK (*fn)(s32) = func_80034E8C_35A8C;
    if (M2C_FIELD(D_80201514_5BD4E4, u16 *, 0x98) != 0) {
        fn(M2C_FIELD(arg0, s32 *, 0xBC));
        M2C_FIELD(arg0, M2C_UNK (**)(void *, s32), 0xC)(arg0, M2C_FIELD(arg0, s32 *, 0x18));
    }
}
