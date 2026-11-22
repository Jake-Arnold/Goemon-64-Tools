#include "m2c_types.h"
extern char func_8000F1E0_FDE0;
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
M2C_UNK func_08000920_6CD5A0();                     /* static */
extern M2C_UNK D_802119E0_5CD9B0;

void func_08001178_6CDDF8(s32 arg0, void *arg1) {
    if (((s32(*)())&func_80023D9C_2499C)(0x16C) == 0) {
        if (!(M2C_FIELD(arg1, u8 *, 0x7C) & 2)) {
            if ((f64) M2C_FIELD(arg1, f32 *, 0x28) == 16.0) {
                ((M2C_UNK(*)())&func_8000F1E0_FDE0)(0x164, &D_802119E0_5CD9B0, arg1, 0x44960000);
            }
        } else {
            ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08000920_6CD5A0);
        }
    }
}
