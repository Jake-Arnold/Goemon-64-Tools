#include "m2c_types.h"
M2C_UNK func_0800281C_6D876C(s32);                  /* extern */
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern char func_8021BB04_5D6FD4;
extern char func_8021C628_5D7AF8;
extern M2C_UNK func_08002CE4_6D8C34;

void func_08002C18_6D8B68(void *arg0, s32 arg1) {
    M2C_FIELD(arg0, s8 *, 0xDC) = 5;
    if (((s32  (*)(void *, M2C_UNK))&func_8021C628_5D7AF8)(arg0, 0x40000000) != 0) {
        func_0800281C_6D876C(arg1);
    }
    if (((s32 (*)(void *, f32, f32, M2C_UNK))&func_8021BB04_5D6FD4)(arg0, (f32) M2C_FIELD(arg0, s16 *, 0xA0), (f32) M2C_FIELD(arg0, s16 *, 0xA2), 0x40000000) == 0) {
        ((M2C_UNK (*)(void *, M2C_UNK, M2C_UNK, M2C_UNK))&func_8021664C_5D1B1C)(arg0, 0, 0x3EAAAAAB, 1);
        M2C_FIELD(arg0, s8 *, 0xDC) = 1;
        M2C_FIELD(arg0, s16 *, 0xDE) = 0;
        ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_08002CE4_6D8C34);
    }

    *(volatile s32 *)0x80000000 = 1;
}
