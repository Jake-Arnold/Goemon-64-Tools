#include "m2c_types.h"
extern char func_080007C0_6D6710;
extern char func_8003521C_35E1C;
extern char func_802197D8_5D4CA8;
extern M2C_UNK func_08000B10_6D6A60;

void func_08000A9C_6D69EC(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_080007C0_6D6710)();
    M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    if (((s32(*)())&func_802197D8_5D4CA8)(arg0, 8) == 0) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x64;
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_08000B10_6D6A60);
    }
}
