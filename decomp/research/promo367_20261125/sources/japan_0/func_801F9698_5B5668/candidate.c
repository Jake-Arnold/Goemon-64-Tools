#include "m2c_types.h"
extern char func_8001B13C_1BD3C;
M2C_UNK func_80038838_39438(M2C_UNK);
M2C_UNK func_801E019C_59C16C(void *, M2C_UNK);
M2C_UNK func_801E6ED8_5A2EA8();
M2C_UNK func_801EDA24_5A99F4(void *, M2C_UNK);

void func_801F9698_5B5668(void *arg0, void *arg1) {
    void *temp_v0;

    func_801E6ED8_5A2EA8();
    if ((((f32(*)())&func_8001B13C_1BD3C)(arg1) - 1.0f) <= M2C_FIELD(arg1, f32 *, 0x28)) {
        if (M2C_FIELD(arg0, u16 *, 0x98) != 0) {
            M2C_FIELD(arg0, f32 *, 0xE4) = 0.0f;
            M2C_FIELD(arg0, f32 *, 0xE8) = 0.0f;
            M2C_FIELD(arg0, f32 *, 0x70) = 0.0f;
            M2C_FIELD(arg0, f32 *, 0x6C) = 0.0f;
            M2C_FIELD(arg0, f32 *, 0x68) = 0.0f;
            func_801E019C_59C16C(arg0, 0x71);
        } else {
            temp_v0 = M2C_FIELD(arg0, void **, 0x5C);
            M2C_FIELD(temp_v0, u16 *, 0x34) = (u16) M2C_FIELD(temp_v0, u16 *, 0x1A);
            func_801E019C_59C16C(arg0, 0x76);
        }
        func_801EDA24_5A99F4(arg0, 2);
        func_80038838_39438(0x205);
        func_80038838_39438(0x20B);
    }
}
