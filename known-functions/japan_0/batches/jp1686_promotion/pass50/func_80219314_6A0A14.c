#include "m2c_types.h"
void *func_80219314_6A0A14(void *arg0, s32 arg1) {
    void *pointer_v0 = M2C_FIELD(arg0, void **, 0x18);
    M2C_FIELD(pointer_v0, s32 *, 0x2C) = (s32) (arg1 + 0x40000000);

    return pointer_v0;
}
