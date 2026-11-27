#include "m2c_types.h"
s32 func_8000DB18_E718(M2C_UNK);                    /* extern */
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
s32 func_801D9238_603CB8(void *, f32, M2C_UNK);             /* extern */
M2C_UNK func_802092F0_633D70(void *, s32);          /* extern */
M2C_UNK func_8020B330_635DB0(void *);               /* extern */
extern void *func_80214670_5CFC00;
extern M2C_UNK func_8020AF3C_6359BC;
extern M2C_UNK func_8020AFE0_635A60;

void func_8020AE64_6358E4(void *arg0, void *arg1) {
    if (func_801D9238_603CB8(arg0, M2C_FIELD(arg1, f32 *, 0x20) * 100.0f, 0xA) != 0) {
        func_802092F0_633D70(arg0, ((func_8000DB18_E718(0x28) / 10) + 0x12) & 0xFF);
        M2C_FIELD(arg0, s32 *, 0x7C) = (s32) (func_8000DB18_E718(0x64) + 0x50);
        M2C_FIELD(arg0, s32 *, 0x80) = 0x96;
        func_80034E8C_35A8C(&func_8020AF3C_6359BC);
    }
    if (M2C_FIELD(func_80214670_5CFC00, u8 *, 0x11) == 2) {
        func_80034E8C_35A8C(&func_8020AFE0_635A60);
        M2C_FIELD(arg0, s32 *, 0x88) = (s32) (M2C_FIELD(arg0, s32 *, 0x84) * 0x1E);
    }
    func_8020B330_635DB0(arg0);

    *(volatile s32 *)0x80000000 = 1;
}
