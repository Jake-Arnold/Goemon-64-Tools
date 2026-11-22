#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D8BF0_603670(void *, M2C_UNK *, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_801D9238_603CB8(void *, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_801D9620_6040A0(void *, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_801DB78C_60620C();                     /* extern */
M2C_UNK func_801EB9BC_61643C();                     /* static */
M2C_UNK func_801F45F0_61F070(void *);               /* static */
extern M2C_UNK D_802107C4_63B244;
extern f64 D_802136F8_63E178;

void func_801EB8D8_616358(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, f32 *, 0x10) >= -500.0f) {
        M2C_FIELD(arg0, f32 *, 0x78) = -8.0f;
        func_801DB78C_60620C();
    }
    M2C_FIELD(arg1, f32 *, 0x28) = (f32) ((f64) M2C_FIELD(arg1, f32 *, 0x28) + D_802136F8_63E178);
    if (M2C_FIELD(arg1, f32 *, 0x28) >= 10.0f) {
        M2C_FIELD(arg1, f32 *, 0x28) = 10.0f;
        func_801D8BF0_603670(arg1, &D_802107C4_63B244, 0, 0);
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x41;
        func_80034E8C_35A8C(func_801EB9BC_61643C);
    }
    func_801D9238_603CB8(arg0, 0x42A00000, 8);
    func_801D9620_6040A0(arg0, 0, 8);
    func_801F45F0_61F070(arg0);
}
