#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_80037890_38490(M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_8003790C_3850C(M2C_UNK, M2C_UNK);      /* extern */
M2C_UNK func_80038838_39438(M2C_UNK);               /* extern */
void *func_801E608C_610B0C(M2C_UNK, s32, M2C_UNK, f32); /* extern */
M2C_UNK func_801F3D88_61E808();                     /* extern */
M2C_UNK func_801FF9F0_62A470();                     /* static */
extern void *D_80214600_63F080;
extern void *D_80214660_63F0E0;

void func_801FF920_62A3A0(void *arg0, M2C_UNK arg1) {
    void *sp1C;

    sp1C = M2C_FIELD(M2C_FIELD(D_80214600_63F080, void **, 0x1D8), void **, 0x18);
    func_801F3D88_61E808();
    if (M2C_FIELD(D_80214600_63F080, u8 *, 0x2C1) == 3) {
        func_80038838_39438(0x10A);
        func_8003790C_3850C(0, 0x3E8);
        func_80037890_38490(0, 1, -1);
        M2C_FIELD(D_80214660_63F0E0, s8 *, 0xC) = 1;
        M2C_FIELD(arg0, s32 *, 0x90) = (s32) M2C_FIELD(func_801E608C_610B0C(3, M2C_FIELD(sp1C, s32 *, 8), 0xC2B40000, M2C_FIELD(sp1C, f32 *, 0x10) + 75.0f), s32 *, 0x18);
        M2C_FIELD(arg0, f32 *, 0x94) = 0.0f;
        func_80034E8C_35A8C(func_801FF9F0_62A470);
    }
}
