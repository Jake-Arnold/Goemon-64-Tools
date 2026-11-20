#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D2EF0_6413E0(void *, M2C_UNK *, M2C_UNK, M2C_UNK, s32, s32, s32, s32); /* extern */
M2C_UNK func_801D95F0_647AE0();                     /* static */
extern M2C_UNK D_801EE200_65C6F0;
extern M2C_UNK D_801F3B48_662038;

void func_801D9550_647A40(void *arg0, void *arg1) {
    M2C_FIELD(arg1, s32 *, 0x2C) = 0;
    M2C_FIELD(arg1, M2C_UNK **, 0x30) = &D_801F3B48_662038;
    M2C_FIELD(arg1, s16 *, 0x14) = 0x100;
    M2C_FIELD(arg1, s16 *, 0x16) = 0;
    M2C_FIELD(arg1, s16 *, 0x18) = 0;
    M2C_FIELD(arg1, f32 *, 0x28) = 0.0f;
    func_801D2EF0_6413E0(arg1, &D_801EE200_65C6F0, 0, 2, 2, 0, (s32) M2C_FIELD(arg1, u16 *, 0x34), 8);
    M2C_FIELD(arg0, f32 *, 0x5C) = 400.0f;
    func_80034E8C_35A8C(func_801D95F0_647AE0);
}
