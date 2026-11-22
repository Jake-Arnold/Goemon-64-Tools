#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_80037890_38490(M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_8003790C_3850C(M2C_UNK, M2C_UNK);      /* extern */
M2C_UNK func_80038838_39438(M2C_UNK);               /* extern */
void *func_801E608C_610B0C(M2C_UNK, s32, M2C_UNK, f32); /* extern */
M2C_UNK func_801F3D88_61E808();                     /* extern */
M2C_UNK func_8020E6E4_639164();                     /* static */
extern void *D_80214600_63F080;

void func_8020E624_6390A4(void *arg0, M2C_UNK arg1) {
    void *sp1C;

    sp1C = M2C_FIELD(M2C_FIELD(D_80214600_63F080, void **, 0x1D8), void **, 0x18);
    func_801F3D88_61E808();
    if (M2C_FIELD(D_80214600_63F080, u8 *, 0x2C1) == 3) {
        func_80038838_39438(0x10A);
        func_8003790C_3850C(0, 0x64);
        func_80037890_38490(0, 1, -1);
        M2C_FIELD(arg0, s32 *, 0x90) = (s32) M2C_FIELD(func_801E608C_610B0C(3, M2C_FIELD(sp1C, s32 *, 8), 0xC1200000, M2C_FIELD(sp1C, f32 *, 0x10) + 20.0f), s32 *, 0x18);
        M2C_FIELD(arg0, f32 *, 0x94) = 0.0f;
        func_80034E8C_35A8C(func_8020E6E4_639164);
    }
}
