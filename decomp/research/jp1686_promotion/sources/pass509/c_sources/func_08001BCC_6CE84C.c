#include "m2c_types.h"
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
M2C_UNK func_08000920_6CD5A0();                     /* static */

void func_08001BCC_6CE84C(s32 arg0, void *arg1) {
    f64 temp_f0;

    if (((s32(*)())&func_80023D9C_2499C)(0x16C) == 0) {
        if (!(M2C_FIELD(arg1, u8 *, 0x7C) & 2)) {
            temp_f0 = (f64) M2C_FIELD(arg1, f32 *, 0x28);
            if ((temp_f0 > 1.0) && (temp_f0 < 4.0)) {
                M2C_FIELD(arg1, u16 *, 0x16) = (u16) (M2C_FIELD(arg1, u16 *, 0x16) + 4);
            }
        } else {
            ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08000920_6CD5A0, arg1);
        }
    }
}
