#include "m2c_types.h"
extern char func_8000F1E0_FDE0;
extern char func_80023CF8_248F8;
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
extern char func_8021B3BC_5D694C;
extern char func_8021DB3C_5D90CC;
M2C_UNK func_080016E0_6CE360();                     /* static */
extern f64 D_08006DA0_6D3A20;
extern M2C_UNK D_802119E0_5CD9B0;

void func_080015C8_6CE248(void *arg0, void *arg1) {
    f32 temp_f0;

    if (((s32(*)())&func_80023D9C_2499C)(0x16C) == 0) {
        temp_f0 = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0xD8) - D_08006DA0_6D3A20);
        M2C_FIELD(arg0, f32 *, 0xD8) = temp_f0;
        M2C_FIELD(arg1, f32 *, 0xC) = (f32) (M2C_FIELD(arg1, f32 *, 0xC) + temp_f0);
        if (M2C_FIELD(arg1, f32 *, 0xC) < 310.0f) {
            ((M2C_UNK(*)())&func_80023CF8_248F8)(0x167);
            ((M2C_UNK(*)())&func_8000F1E0_FDE0)(0x2A2, &D_802119E0_5CD9B0, arg1, 0x44960000);
            M2C_FIELD(arg1, f32 *, 0xC) = 310.0f;
            M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
            M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
            M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
            ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 6, 0x3E800000, 4);
            ((M2C_UNK(*)())&func_8021DB3C_5D90CC)(arg0, 7);
            ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_080016E0_6CE360);
        }
    }
}
