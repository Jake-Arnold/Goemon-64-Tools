#include "m2c_types.h"
void *func_80035558_36158(void *, void *, s32, s32, f32, f32, f32, s32, s32, s32, f32, f32, f32, s32, s32);
void func_801D8DE4_603864(void *);
extern u8 *D_80214600_63F080;
extern M2C_UNK func_801FD14C_627BCC;

void *func_801FD088_627B08(void) {
    void *ret;

    ret = func_80035558_36158(
        M2C_FIELD(D_80214600_63F080, void **, 0x1D8), &func_801FD14C_627BCC, 0, 0,
        M2C_FIELD(M2C_FIELD(M2C_FIELD(D_80214600_63F080, void **, 0x1D8), void **, 0x18), f32 *, 8),
        M2C_FIELD(M2C_FIELD(M2C_FIELD(D_80214600_63F080, void **, 0x1D8), void **, 0x18), f32 *, 0xC),
        M2C_FIELD(M2C_FIELD(M2C_FIELD(D_80214600_63F080, void **, 0x1D8), void **, 0x18), f32 *, 0x10),
        0, 0, 0,
        M2C_FIELD(M2C_FIELD(M2C_FIELD(D_80214600_63F080, void **, 0x1D8), void **, 0x18), f32 *, 0x1C),
        M2C_FIELD(M2C_FIELD(M2C_FIELD(D_80214600_63F080, void **, 0x1D8), void **, 0x18), f32 *, 0x20),
        M2C_FIELD(M2C_FIELD(M2C_FIELD(D_80214600_63F080, void **, 0x1D8), void **, 0x18), f32 *, 0x24),
        0, 0);
    if (ret != NULL) {
        M2C_FIELD(ret, s8 *, 0x30) = 2;
        M2C_FIELD(ret, s32 *, 0x48) = -1;
        M2C_FIELD(ret, s8 *, 0x4C) = 0x54;
        M2C_FIELD(ret, s16 *, 0x4E) = 0x190;
        M2C_FIELD(ret, s16 *, 0x50) = 0x32;
        M2C_FIELD(ret, s16 *, 0x52) = 0;
        func_801D8DE4_603864(ret);
    }
    return ret;
}
