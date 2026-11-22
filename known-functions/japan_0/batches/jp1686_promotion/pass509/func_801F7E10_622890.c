#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D8738_6031B8(void *, M2C_UNK);      /* extern */
M2C_UNK func_801D88EC_60336C(void *, M2C_UNK *);    /* extern */
u8 func_801D9238_603CB8(void *, f32, M2C_UNK);      /* extern */
M2C_UNK func_801D9620_6040A0(void *, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_801F7EB8_622938();                     /* static */
s32 func_801FCA5C_6274DC(void *);                   /* static */
extern M2C_UNK D_802109C8_63B448;

void func_801F7E10_622890(void *arg0, void *arg1) {
    u8 sp27;

    func_801D8738_6031B8(arg1, 0x42200000);
    func_801D9620_6040A0(arg0, 0, 8);
    sp27 = func_801D9238_603CB8(arg0, M2C_FIELD(arg1, f32 *, 0x20) * 300.0f, 0x10);
    if ((func_801FCA5C_6274DC(arg0) != 0) && (sp27 != 0)) {
        M2C_FIELD(arg0, s32 *, 0x7C) = 0xC8;
        func_801D88EC_60336C(arg0, &D_802109C8_63B448);
        func_80034E8C_35A8C(func_801F7EB8_622938);
    }
}
