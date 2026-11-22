#include "m2c_types.h"
M2C_UNK func_80037890_38490(M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_8003790C_3850C(M2C_UNK, M2C_UNK);      /* extern */
M2C_UNK func_80038838_39438(M2C_UNK);               /* extern */
M2C_UNK func_801E4FA4_60FA24(s32, s32, s32, s32, f32); /* static */
extern f32 D_80213088_63DB08;
extern f32 D_8021308C_63DB0C;
extern void *D_80214600_63F080;

void func_801E0630_60B0B0(void *arg0, s32 arg1) {
    if (arg1 == M2C_FIELD(D_80214600_63F080, s32 *, 0x1D8)) {
        func_80038838_39438(0x24F);
        func_8003790C_3850C(0, 0xA);
        func_80037890_38490(0, 1, -1);
        M2C_FIELD(arg0, s8 *, 0x30) = 0;
        func_801E4FA4_60FA24(M2C_FIELD(D_80214600_63F080, s32 *, 0x1C8), M2C_FIELD(arg0, s32 *, 0xD0), M2C_FIELD(arg0, s32 *, 0xD4), M2C_FIELD(arg0, s32 *, 0xD8), D_80213088_63DB08);
        return;
    }
    M2C_FIELD(arg0, s8 *, 0x30) = 0;
    func_801E4FA4_60FA24(M2C_FIELD(D_80214600_63F080, s32 *, 0x1C8), M2C_FIELD(arg0, s32 *, 0xD0), M2C_FIELD(arg0, s32 *, 0xD4), M2C_FIELD(arg0, s32 *, 0xD8), D_8021308C_63DB0C);
}
