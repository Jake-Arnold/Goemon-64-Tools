#include "m2c_types.h"
extern M2C_UNK func_80023D48_24948;

void func_802267B0_5E1D40(void) {
    void (*fn)(s32) = (void (*)(s32))&func_80023D48_24948;
    s32 var_s0;

    for (var_s0 = 0x9C; var_s0 != 0xA1; var_s0++) {
        fn(var_s0);
    }
}
