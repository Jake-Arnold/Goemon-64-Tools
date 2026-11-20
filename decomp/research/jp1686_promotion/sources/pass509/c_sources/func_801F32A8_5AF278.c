#include "m2c_types.h"
void func_801F32A8_5AF278(void *arg0, void *arg1) {
    if ((arg0 != NULL) && (arg1 != NULL)) {
        M2C_FIELD(arg1, f32 *, 0x1C) = (f32) M2C_FIELD(arg0, f32 *, 0x1C);
        M2C_FIELD(arg1, f32 *, 0x20) = (f32) M2C_FIELD(arg0, f32 *, 0x20);
        M2C_FIELD(arg1, f32 *, 0x24) = (f32) M2C_FIELD(arg0, f32 *, 0x24);
    }
}
