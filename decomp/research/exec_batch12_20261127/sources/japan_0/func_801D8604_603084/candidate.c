#include "m2c_types.h"

void func_80013DA8_149A8(void *);

void func_801D8604_603084(void *arg0, void *arg1) {
    if (arg0 != NULL) {
        M2C_FIELD(arg0, s32 *, 0x2C) = M2C_FIELD(arg1, s32 *, 0);
        M2C_FIELD(arg0, f32 *, 0x28) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x94) = (f32)(u32)M2C_FIELD(arg1, u8 *, 4);
        M2C_FIELD(arg0, u16 *, 0x34) = M2C_FIELD(arg1, u16 *, 6);
        func_80013DA8_149A8(arg0);
    }
}
