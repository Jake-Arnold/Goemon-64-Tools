#include "../m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D8604_603084(s32, M2C_UNK *);       /* extern */
M2C_UNK func_801F9F90_624A10();                     /* static */
M2C_UNK func_801FC7A4_627224();                     /* static */
extern M2C_UNK D_80210A00_63B480;

void func_801F9EB0_624930(void *arg0, s32 arg1) {
    func_801FC7A4_627224();
    M2C_FIELD(arg0, f32 *, 0x74) = 7.0f;
    func_801D8604_603084(arg1, &D_80210A00_63B480);
    M2C_FIELD(arg0, s32 *, 0xE8) = (s32) (M2C_FIELD(arg0, s32 *, 0xE8) + 1);
    func_80034E8C_35A8C(func_801F9F90_624A10);
}
