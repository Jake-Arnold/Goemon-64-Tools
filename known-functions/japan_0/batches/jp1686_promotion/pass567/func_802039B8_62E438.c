#include "../m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_80038838_39438(M2C_UNK);               /* extern */
M2C_UNK func_801D8604_603084(s32, M2C_UNK *);       /* extern */
M2C_UNK func_80203A38_62E4B8();                     /* static */
M2C_UNK func_8020559C_63001C();                     /* static */
extern M2C_UNK D_80210B68_63B5E8;
extern void *func_80214670_5CFC00;

void func_802039B8_62E438(void *arg0, s32 arg1) {
    func_8020559C_63001C();
    M2C_FIELD(func_80214670_5CFC00, s8 *, 0x815) = 0;
    M2C_FIELD(arg0, s32 *, 0x80) = 0x92;
    M2C_FIELD(arg0, s32 *, 0x7C) = 0x92;
    M2C_FIELD(arg0, f32 *, 0x74) = 14.0f;
    func_801D8604_603084(arg1, &D_80210B68_63B5E8);
    func_80038838_39438(0x34E);
    M2C_FIELD(arg0, s32 *, 0xE8) = (s32) (M2C_FIELD(arg0, s32 *, 0xE8) + 1);
    func_80034E8C_35A8C(func_80203A38_62E4B8);
}
