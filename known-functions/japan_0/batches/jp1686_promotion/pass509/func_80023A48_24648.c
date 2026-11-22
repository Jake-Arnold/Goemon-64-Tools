#include "m2c_types.h"
M2C_UNK func_80023598_24198();                      /* extern */

void func_80023A48_24648(void) {
    s32 var_a0;
    s32 var_v0;

    func_80023598_24198();
    var_a0 = 0;
    do {
        var_v0 = 0;
loop_2:
        var_v0 += 4;
        if (var_v0 != 0x10) {
            goto loop_2;
        }
        var_a0 += 1;
    } while (var_a0 != 0x10);
}
