#include "m2c_types.h"
void func_8000D928_E528(void *arg0, f32 arg1) {
    M2C_FIELD(arg0, f32 *, 0x20) = (f32) (M2C_FIELD(arg0, f32 *, 0x20) + arg1);
    if (M2C_FIELD(arg0, f32 *, 0x20) > 100.0f) {
        M2C_FIELD(arg0, f32 *, 0x20) = 100.0f;
    }
    M2C_FIELD(arg0, f32 *, 0x24) = (f32) (M2C_FIELD(arg0, f32 *, 0x20) + M2C_FIELD(arg0, f32 *, 0x24));
}
