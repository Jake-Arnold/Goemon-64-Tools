#include "m2c_types.h"
extern char func_80023D48_24948;
extern char func_80023D9C_2499C;
extern char func_80034E8C_35A8C;
extern char func_8021B3BC_5D694C;
extern M2C_UNK func_08002A24_6B6924;
extern M2C_UNK func_08002DE0_6B6CE0;

void func_08002948_6B6848(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s32 *, 0x60) = 0x80000220;
    M2C_FIELD(arg0, s8 *, 0x6C) = 0;
    M2C_FIELD(arg0, s32 *, 0xD0) = 0;
    if (((s32 (*)(M2C_UNK))&func_80023D9C_2499C)(0x98) != 0) {
        M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 0x01000001);
        ((M2C_UNK  (*)(void *, M2C_UNK, f32, M2C_UNK))&func_8021B3BC_5D694C)(arg0, 0, 0.0f, 0);
        ((M2C_UNK (*)(M2C_UNK *))&func_80034E8C_35A8C)(&func_08002DE0_6B6CE0);
        return;
    }
    ((M2C_UNK  (*)(void *, M2C_UNK, f32, M2C_UNK))&func_8021B3BC_5D694C)(arg0, 0, 0.0f, 1);
    ((M2C_UNK (*)(M2C_UNK))&func_80023D48_24948)(0x5D);
    ((M2C_UNK (*)(M2C_UNK *))&func_80034E8C_35A8C)(&func_08002A24_6B6924);

    *(volatile s32 *)0x80000000 = 1;
}
