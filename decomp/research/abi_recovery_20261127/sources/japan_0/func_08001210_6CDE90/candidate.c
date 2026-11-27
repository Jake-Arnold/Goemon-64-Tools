#include "m2c_types.h"
extern char _nsqrtf;
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
extern char func_8021B3BC_5D694C;
extern char func_8021DB3C_5D90CC;
extern char func_8021E548_5D9AD8;
extern M2C_UNK func_08001310_6CDF90;

void func_08001210_6CDE90(void *arg0, void *arg1) {
    f32 temp_f0;
    f32 temp_f2;
    void *temp_v0;

    if ((((s32 (*)(M2C_UNK))&func_80023D9C_2499C)(0x16C) == 0) && (((s32 (*)(void *, M2C_UNK))&func_8021E548_5D9AD8)(arg0, 0x10) == 0)) {
        temp_v0 = M2C_FIELD(arg0, void **, 0x84);
        M2C_FIELD(arg0, f32 *, 0xD8) = 10.0f;
        temp_f0 = M2C_FIELD(temp_v0, f32 *, 0x10) - M2C_FIELD(arg1, f32 *, 0x10);
        temp_f2 = M2C_FIELD(temp_v0, f32 *, 8) - M2C_FIELD(arg1, f32 *, 8);
        M2C_FIELD(arg0, f32 *, 0xEC) = (f32) (((f32 (*)(f32))&_nsqrtf)((temp_f0 * temp_f0) + (temp_f2 * temp_f2)) - 55.0f);
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 0x01000000);
        ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_8021B3BC_5D694C)(arg0, 0x10, 0x3F000000, 4);
        ((M2C_UNK (*)(void *, M2C_UNK))&func_8021DB3C_5D90CC)(arg0, 0x11);
        ((M2C_UNK (*)(M2C_UNK *))&func_80034E8C_35A8C)(&func_08001310_6CDF90);
    }
}
