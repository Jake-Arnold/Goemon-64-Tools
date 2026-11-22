#include "m2c_types.h"
M2C_UNK func_8000E5C8_F1C8(u16, u16, u16, void *, void *, void *); /* extern */
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_80205DB4_630834();                     /* static */
M2C_UNK func_802069F8_631478();                     /* static */
M2C_UNK func_802097AC_63422C(void *);               /* static */
extern s8 *func_80214670_5CFC00;

void func_80206948_6313C8(s8 *arg0, s8 *arg1) {
    if ((s32) M2C_FIELD(func_80214670_5CFC00, u8 *, 8) >= 6) {
        func_80205DB4_630834();
        return;
    }
    M2C_FIELD(func_80214670_5CFC00, s8 *, 7) = 1;
    M2C_FIELD(arg0, s32 *, 0x7C) = 6;
    M2C_FIELD(arg0, f32 *, 0x70) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x74) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x78) = -8.0f;
    func_8000E5C8_F1C8(M2C_FIELD(arg1, u16 *, 0x14), M2C_FIELD(arg1, u16 *, 0x16), M2C_FIELD(arg1, u16 *, 0x18), arg0 + 0x70, arg0 + 0x74, arg0 + 0x78);
    func_80034E8C_35A8C(func_802069F8_631478);
    func_802097AC_63422C(arg0);
}
