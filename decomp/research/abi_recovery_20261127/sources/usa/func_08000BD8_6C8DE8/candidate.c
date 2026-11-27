#include "m2c_types.h"
extern char _nsqrtf;
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern char func_80218DCC_5D429C;
extern char func_802197D8_5D4CA8;
extern M2C_UNK func_08000CCC_6C8EDC;

void func_08000BD8_6C8DE8(void *arg0, void *arg1) {
    f32 temp_f0;
    f32 temp_f2;
    void *temp_v0;

    if ((((s32 (*)(M2C_UNK))&func_800240DC_24CDC)(0x16C) == 0) && (((s32 (*)(void *, M2C_UNK))&func_802197D8_5D4CA8)(arg0, 0x10) == 0)) {
        temp_v0 = M2C_FIELD(arg0, void **, 0x84);
        temp_f0 = M2C_FIELD(temp_v0, f32 *, 0x10) - M2C_FIELD(arg1, f32 *, 0x10);
        temp_f2 = M2C_FIELD(temp_v0, f32 *, 8) - M2C_FIELD(arg1, f32 *, 8);
        M2C_FIELD(arg0, f32 *, 0xEC) = (f32) (((f32 (*)(f32))&_nsqrtf)((temp_f0 * temp_f0) + (temp_f2 * temp_f2)) - 50.0f);
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 0x01000000);
        ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_8021664C_5D1B1C)(arg0, 0x10, 0x3F000000, 4);
        ((M2C_UNK (*)(void *, M2C_UNK))&func_80218DCC_5D429C)(arg0, 0x11);
        ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_08000CCC_6C8EDC);
    }
}
