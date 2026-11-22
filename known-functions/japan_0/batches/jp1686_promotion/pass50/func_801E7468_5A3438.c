#include "m2c_types.h"
M2C_UNK func_801E2BE0_59EBB0(void *, M2C_UNK);              /* extern */
extern f32 D_80210188_5CC158;

void func_801E7468_5A3438(void *arg0) {
    M2C_FIELD(arg0, f32 *, 0xA4) = (f32) D_80210188_5CC158;
    M2C_FIELD(arg0, f32 *, 0x6C) = 0.0f;
    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s16 *, 0x30) = 0;
    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s8 *, 0x2E) = 0;
    func_801E2BE0_59EBB0(arg0, 1);
}
