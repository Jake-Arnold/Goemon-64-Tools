#include "m2c_types.h"
extern M2C_UNK func_80024088_24C88;

void func_80221A40_5DCF10(void) {
    void (*fn)(s32) = (void (*)(s32))&func_80024088_24C88;
    s32 var_s0;

    for (var_s0 = 0x9C; var_s0 != 0xA1; var_s0++) {
        fn(var_s0);
    }
}
