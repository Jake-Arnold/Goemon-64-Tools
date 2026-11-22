#include "m2c_types.h"
extern char func_8000F1E0_FDE0;
extern char func_80034E8C_35A8C;
M2C_UNK func_08001B04_6C5CC4();                     /* static */
extern M2C_UNK D_802119E0_5CD9B0;

void func_08001A7C_6C5C3C(void *arg0, void *arg1) {
    if (!(M2C_FIELD(arg1, f32 *, 0xC) > -33.0f)) {
        ((M2C_UNK(*)())&func_8000F1E0_FDE0)(0x272, &D_802119E0_5CD9B0, arg1, 0x461C4000);
        M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
        M2C_FIELD(arg1, f32 *, 0xC) = -33.0f;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08001B04_6C5CC4);
    }
}
