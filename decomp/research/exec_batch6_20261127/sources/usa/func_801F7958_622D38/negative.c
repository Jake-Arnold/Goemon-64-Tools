#include "m2c_types.h"
void *func_800358E8_364E8(void *, void *, s32, s32, f32, f32, f32, s32, s32, s32, f32, f32, f32, s32, s32);
void func_801D36C4_5FEAA4(void *);
extern u8 *D_8020EED0_63A2B0;
extern M2C_UNK func_801F7A1C_622DFC;

void *func_801F7958_622D38(void) {
    void *ret;

    ret = func_800358E8_364E8(
        M2C_FIELD(D_8020EED0_63A2B0, void **, 0x1D8), &func_801F7A1C_622DFC, 0, 0,
        M2C_FIELD(M2C_FIELD(M2C_FIELD(D_8020EED0_63A2B0, void **, 0x1D8), void **, 0x18), f32 *, 8),
        M2C_FIELD(M2C_FIELD(M2C_FIELD(D_8020EED0_63A2B0, void **, 0x1D8), void **, 0x18), f32 *, 0xC),
        M2C_FIELD(M2C_FIELD(M2C_FIELD(D_8020EED0_63A2B0, void **, 0x1D8), void **, 0x18), f32 *, 0x10),
        0, 0, 0,
        M2C_FIELD(M2C_FIELD(M2C_FIELD(D_8020EED0_63A2B0, void **, 0x1D8), void **, 0x18), f32 *, 0x1C),
        M2C_FIELD(M2C_FIELD(M2C_FIELD(D_8020EED0_63A2B0, void **, 0x1D8), void **, 0x18), f32 *, 0x20),
        M2C_FIELD(M2C_FIELD(M2C_FIELD(D_8020EED0_63A2B0, void **, 0x1D8), void **, 0x18), f32 *, 0x24),
        0, 0);
    if (ret != NULL) {
        M2C_FIELD(ret, s8 *, 0x30) = 2;
        M2C_FIELD(ret, s32 *, 0x48) = -1;
        M2C_FIELD(ret, s8 *, 0x4C) = 0x54;
        M2C_FIELD(ret, s16 *, 0x4E) = 0x190;
        M2C_FIELD(ret, s16 *, 0x50) = 0x32;
        M2C_FIELD(ret, s16 *, 0x52) = 0;
        func_801D36C4_5FEAA4(ret);
    }
    { *(volatile s32 *)0x80000000 = 1; } return ret;
}
