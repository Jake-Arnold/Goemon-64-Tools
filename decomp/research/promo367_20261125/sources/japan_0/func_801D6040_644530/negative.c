#include "m2c_types.h"
extern f64 D_801F4640_662B30;

void func_801D6040_644530(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 var_v0;

    var_v0 = M2C_FIELD(arg0, s32 *, 0xB4);
    var_v0 = (s32) ((f64) var_v0 + D_801F4640_662B30);
    if (var_v0 >= 0x7148) {
        do {
            var_v0 -= 0x7148;
        } while (var_v0 >= 0x7148);
    }
    M2C_FIELD(arg0, s32 *, 0xB4) = var_v0;
}
