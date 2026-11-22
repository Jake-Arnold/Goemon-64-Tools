#include "m2c_types.h"
M2C_UNK func_801D6040_644530();                     /* static */
M2C_UNK func_801D6090_644580();                     /* static */
M2C_UNK func_801D60DC_6445CC();                     /* static */
M2C_UNK func_801D6128_644618();                     /* static */

void func_801D5F80_644470(void *arg0) {
    s32 temp_v0_2;
    s8 temp_v0;

    temp_v0 = M2C_FIELD(arg0, s8 *, 0x9F);
    if (temp_v0 & 1) {
        M2C_FIELD(arg0, s8 *, 0x9F) = (s8) (temp_v0 & 0xFFFE);
        M2C_FIELD(arg0, s32 *, 0xB0) = 0;
    }
    M2C_FIELD(arg0, s8 *, 0xA2) = 0x14;
    if (M2C_FIELD(arg0, u8 *, 0x9E) == 0) {
        M2C_FIELD(arg0, s8 *, 0x9D) = 1;
        func_801D6040_644530();
        if (M2C_FIELD(arg0, s8 *, 0xC4) != 0) {
            M2C_FIELD(arg0, s8 *, 0xC4) = 0;
            M2C_FIELD(arg0, s32 *, 0xB4) = 0x2710;
        }
    } else {
        temp_v0_2 = M2C_FIELD(arg0, s32 *, 0xB4);
        if (temp_v0_2 < 0x3A99) {
            M2C_FIELD(arg0, s8 *, 0x9D) = 2;
            func_801D6090_644580();
            return;
        }
        if (temp_v0_2 < 0x4651) {
            M2C_FIELD(arg0, s8 *, 0x9D) = 3;
            func_801D60DC_6445CC();
            return;
        }
        M2C_FIELD(arg0, s8 *, 0x9D) = 4;
        func_801D6128_644618();
    }
}
