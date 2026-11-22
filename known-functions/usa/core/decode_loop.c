#include "common.h"
s32 func_80014CC4_158C4(s32);
s32 func_80015EFC_16AFC(void) {
    s32 var_s0;
    var_s0 = 1;
    if (func_80014CC4_158C4(1) != 0) {
        do {
            var_s0 += 1;
        } while (func_80014CC4_158C4(1) != 0);
    }
    return (func_80014CC4_158C4(var_s0) + (1 << var_s0)) - 1;
}
#pragma GLOBAL_ASM("asm/usa/nonmatchings/decode_loop/func_80015F58_16B58.s")
