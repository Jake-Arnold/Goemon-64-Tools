#include "m2c_types.h"
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
M2C_UNK func_08005090_6C47E0();                     /* static */

void func_08005018_6C4768(void *arg0, void *arg1) {
    if (((s32(*)())&func_800240DC_24CDC)(0xA4) == 0) {
        M2C_FIELD(arg0, s16 *, 0x5E) = 0x350;
        M2C_FIELD(arg1, f32 *, 8) = 80.0f;
        M2C_FIELD(arg1, f32 *, 0xC) = 20.0f;
        M2C_FIELD(arg1, f32 *, 0x10) = 0.0f;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08005090_6C47E0, arg1);
    }
}
