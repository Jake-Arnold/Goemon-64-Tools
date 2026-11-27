#include "m2c_types.h"
u16 func_800040A8_4CA8(f32, f32);

u16 func_8000EA34_F634(f32 arg0, f32 arg1, void *arg2) {
    f32 dx = arg0 - M2C_FIELD(arg2, f32 *, 8);
    f32 dy = arg1 - M2C_FIELD(arg2, f32 *, 0xC);
    return func_800040A8_4CA8(dy, dx) & 0x3FF;
}
