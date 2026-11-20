#include "m2c_types.h"
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
extern char func_8021B3BC_5D694C;
extern char func_8021DB3C_5D90CC;
M2C_UNK func_080015C8_6CE248();                     /* static */
extern f64 D_08006D98_6D3A18;

void func_080014F0_6CE170(void *arg0, void *arg1) {
    f32 temp_f0;

    if (((s32(*)())&func_80023D9C_2499C)(0x16C) == 0) {
        temp_f0 = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0xD8) - D_08006D98_6D3A18);
        M2C_FIELD(arg0, f32 *, 0xD8) = temp_f0;
        M2C_FIELD(arg1, f32 *, 0xC) = (f32) (M2C_FIELD(arg1, f32 *, 0xC) + temp_f0);
        if (M2C_FIELD(arg0, f32 *, 0xD8) < 0.0f) {
            M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & 0xFEFFFFFF);
            ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 0xC, 0x3F000000, 4);
            ((M2C_UNK(*)())&func_8021DB3C_5D90CC)(arg0, 0xC);
            ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080015C8_6CE248);
        }
    }
}
