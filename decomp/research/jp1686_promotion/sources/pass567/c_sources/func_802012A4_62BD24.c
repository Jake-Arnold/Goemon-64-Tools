#include "../m2c_types.h"
M2C_UNK func_801D8660_6030E0(void *, M2C_UNK);      /* extern */

void func_802012A4_62BD24(s32 arg0, void *arg1) {
    M2C_FIELD(arg1, f32 *, 0x10) = (f32) ((f64) M2C_FIELD(arg1, f32 *, 0x10) - 0.5);
    func_801D8660_6030E0(arg1, 0x42A00000);
}
