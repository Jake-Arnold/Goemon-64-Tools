#include "m2c_types.h"
M2C_UNK func_8000B760_C360(s32);                    /* extern */

void func_8000B720_C320(void) {
    s32 var_s0;

    var_s0 = 0;
    do {
        func_8000B760_C360(var_s0);
        var_s0 += 1;
    } while (var_s0 != 3);
}
