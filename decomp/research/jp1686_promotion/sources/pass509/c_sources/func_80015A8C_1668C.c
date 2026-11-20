#include "m2c_types.h"
s32 func_80014854_15454(s32);                       /* extern */

s32 func_80015A8C_1668C(void) {
    s32 var_s0;

    var_s0 = 1;
    if (func_80014854_15454(1) != 0) {
        do {
            var_s0 += 1;
        } while (func_80014854_15454(1) != 0);
    }
    return (func_80014854_15454(var_s0) + (1 << var_s0)) - 1;
}
