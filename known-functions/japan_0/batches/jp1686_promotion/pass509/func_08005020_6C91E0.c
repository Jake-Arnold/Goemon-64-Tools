#include "m2c_types.h"
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
M2C_UNK func_08005098_6C9258();                     /* static */

void func_08005020_6C91E0(void *arg0, void *arg1) {
    if (((s32(*)())&func_80023D9C_2499C)(0xA4) == 0) {
        M2C_FIELD(arg0, s16 *, 0x5E) = 0x350;
        M2C_FIELD(arg1, f32 *, 8) = 80.0f;
        M2C_FIELD(arg1, f32 *, 0xC) = 20.0f;
        M2C_FIELD(arg1, f32 *, 0x10) = 0.0f;
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08005098_6C9258, arg1);
    }
}
