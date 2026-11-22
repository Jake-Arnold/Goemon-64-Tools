#include "m2c_types.h"
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
extern char func_8021B3BC_5D694C;
extern char func_8021DB3C_5D90CC;
M2C_UNK func_0800213C_6CEDBC();                     /* static */
extern f64 D_08006DB8_6D3A38;

void func_08002064_6CECE4(void *arg0, void *arg1) {
    f32 temp_f0;

    if (((s32(*)())&func_80023D9C_2499C)(0x16C) == 0) {
        temp_f0 = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0xD8) - D_08006DB8_6D3A38);
        M2C_FIELD(arg0, f32 *, 0xD8) = temp_f0;
        M2C_FIELD(arg1, f32 *, 0xC) = (f32) (M2C_FIELD(arg1, f32 *, 0xC) + temp_f0);
        if (M2C_FIELD(arg0, f32 *, 0xD8) < 0.0f) {
            M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) & 0xFEFFFFFF);
            ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 0x10, 0x3F000000, 4);
            ((M2C_UNK(*)())&func_8021DB3C_5D90CC)(arg0, 0x11);
            ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_0800213C_6CEDBC);
        }
    }
}
