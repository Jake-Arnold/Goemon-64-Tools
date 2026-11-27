#include "m2c_types.h"
extern char func_80012304_12F04;
extern char func_80024088_24C88;
extern char func_800240DC_24CDC;
extern char func_80034EF8_35AF8;
extern char func_8003521C_35E1C;
extern char func_8003F1D8_3FDD8;
extern char func_801FC590_5B84A0;
extern char func_802204FC_5DB9CC;
extern char func_80221FB0_5DD480;
extern void *D_801FC624_5B8534;
extern void *D_801FC628_5B8538;
extern M2C_UNK func_080016B4_718554;
extern M2C_UNK func_08001AE4_718984;

void func_08001980_718820(void *arg0, M2C_UNK arg1) {
    void *temp_s0;

    temp_s0 = M2C_FIELD(arg0, void **, 0xD0);
    ((M2C_UNK  (*)(void *, M2C_UNK))&func_802204FC_5DB9CC)(arg0, 0);
    if (((s32 (*)())&func_8003F1D8_3FDD8)() == 0) {
        if (((s32 (*)(M2C_UNK))&func_800240DC_24CDC)(0x7D) != 0) {
            ((M2C_UNK (*)(M2C_UNK))&func_80024088_24C88)(0x7D);
            ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_08001AE4_718984);
            return;
        }
        M2C_FIELD(M2C_FIELD(temp_s0, void **, 0x10), f32 *, 0) = -32.0f;
        M2C_FIELD(M2C_FIELD(temp_s0, void **, 0x10), f32 *, 4) = 56.0f;
        M2C_FIELD(M2C_FIELD(temp_s0, void **, 0x10), f32 *, 8) = 15.0f;
        M2C_FIELD(M2C_FIELD(temp_s0, void **, 0x10), f32 *, 0xC) = 6.0f;
        M2C_FIELD(M2C_FIELD(temp_s0, void **, 0x10), f32 *, 0x10) = 31.0f;
        M2C_FIELD(M2C_FIELD(temp_s0, void **, 0x10), f32 *, 0x14) = 4.0f;
        M2C_FIELD(M2C_FIELD(temp_s0, void **, 0x10), s16 *, 0x1A) = 0x1840;
        M2C_FIELD(D_801FC624_5B8534, s8 *, 0xD0) = 0x3C;
        ((M2C_UNK (*)(s32))&func_80012304_12F04)(M2C_FIELD(temp_s0, s32 *, 8));
        ((M2C_UNK (*)(s32))&func_80034EF8_35AF8)(M2C_FIELD(temp_s0, s32 *, 0xC));
        M2C_FIELD(D_801FC628_5B8538, s8 *, 0x64) = 0;
        ((M2C_UNK (*)())&func_801FC590_5B84A0)();
        ((M2C_UNK (*)())&func_80221FB0_5DD480)();
        ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_080016B4_718554);
    }
}
