#include "m2c_types.h"
extern char func_80023B54_24754;
extern char func_80034E8C_35A8C;
extern M2C_UNK func_08007398_6BF118;
extern M2C_UNK func_0800794C_6BF6CC;

void func_08007C58_6BF9D8(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u16 *, 0x8A);
    M2C_FIELD(arg0, u16 *, 0x8A) = (u16) (temp_v0 - 1);
    if (temp_v0 == 0) {
        if (((s32(*)())&func_80023B54_24754)(0xB) != 0) {
            ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_0800794C_6BF6CC);
        }
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_08007398_6BF118);
    }
}
