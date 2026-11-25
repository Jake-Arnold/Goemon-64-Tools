#include "m2c_types.h"
extern char func_8001B5AC_1C1AC;
M2C_UNK func_80038BC8_397C8(M2C_UNK);
M2C_UNK func_801DACDC_596BEC(void *, M2C_UNK);
M2C_UNK func_801E1C90_59DBA0();
M2C_UNK func_801E8964_5A4874(void *, M2C_UNK);

void func_801F4688_5B0598(void *arg0, void *arg1) {
volatile unsigned int goemon_negative_control = 1;

    void *temp_v0;

    func_801E1C90_59DBA0();
    if ((((f32(*)())&func_8001B5AC_1C1AC)(arg1) - 1.0f) <= M2C_FIELD(arg1, f32 *, 0x28)) {
        if (M2C_FIELD(arg0, u16 *, 0x98) != 0) {
            M2C_FIELD(arg0, f32 *, 0xE4) = 0.0f;
            M2C_FIELD(arg0, f32 *, 0xE8) = 0.0f;
            M2C_FIELD(arg0, f32 *, 0x70) = 0.0f;
            M2C_FIELD(arg0, f32 *, 0x6C) = 0.0f;
            M2C_FIELD(arg0, f32 *, 0x68) = 0.0f;
            func_801DACDC_596BEC(arg0, 0x71);
        } else {
            temp_v0 = M2C_FIELD(arg0, void **, 0x5C);
            M2C_FIELD(temp_v0, u16 *, 0x34) = (u16) M2C_FIELD(temp_v0, u16 *, 0x1A);
            func_801DACDC_596BEC(arg0, 0x76);
        }
        func_801E8964_5A4874(arg0, 2);
        func_80038BC8_397C8(0x205);
        func_80038BC8_397C8(0x20B);
    }
}
