#include "m2c_types.h"
void func_801F3278_5AF248(void *arg0, void *arg1) {
    if ((arg0 != NULL) && (arg1 != NULL)) {
        M2C_FIELD(arg1, f32 *, 8) = (f32) M2C_FIELD(arg0, f32 *, 8);
        M2C_FIELD(arg1, f32 *, 0xC) = (f32) M2C_FIELD(arg0, f32 *, 0xC);
        M2C_FIELD(arg1, f32 *, 0x10) = (f32) M2C_FIELD(arg0, f32 *, 0x10);
    }
}
