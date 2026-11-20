#include "m2c_types.h"
extern char func_8000F1E0_FDE0;
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
extern char func_8021B3BC_5D694C;
M2C_UNK func_08001ACC_6CE74C();                     /* static */
extern M2C_UNK D_802119E0_5CD9B0;

void func_080019D4_6CE654(void *arg0, void *arg1) {
    f64 temp_f0;

    if (((s32(*)())&func_80023D9C_2499C)(0x16C) == 0) {
        temp_f0 = (f64) M2C_FIELD(arg1, f32 *, 0x28);
        if (temp_f0 < 4.0) {
            if (temp_f0 > 1.0) {
                M2C_FIELD(arg1, u16 *, 0x16) = (u16) (M2C_FIELD(arg1, u16 *, 0x16) - 4);
            }
        } else {
            M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 0x01000000);
            ((M2C_UNK(*)())&func_8021B3BC_5D694C)(arg0, 8, 0x3E800000, 4);
            M2C_FIELD(arg1, f32 *, 0x28) = 4.0f;
            ((M2C_UNK(*)())&func_8000F1E0_FDE0)(0x271, &D_802119E0_5CD9B0, arg1, 0x44960000);
            ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08001ACC_6CE74C);
        }
    }
}
