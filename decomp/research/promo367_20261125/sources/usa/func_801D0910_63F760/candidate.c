#include "m2c_types.h"
extern f64 D_801EEF10_65DD60;

void func_801D0910_63F760(void *arg0, M2C_UNK arg1) {
    s32 var_v0;

    var_v0 = M2C_FIELD(arg0, s32 *, 0xB4);
    var_v0 = (s32) ((f64) var_v0 + D_801EEF10_65DD60);
    if (var_v0 >= 0x7148) {
        do {
            var_v0 -= 0x7148;
        } while (var_v0 >= 0x7148);
    }
    M2C_FIELD(arg0, s32 *, 0xB4) = var_v0;
}
