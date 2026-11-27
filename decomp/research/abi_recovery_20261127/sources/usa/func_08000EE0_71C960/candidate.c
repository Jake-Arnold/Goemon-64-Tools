#include "m2c_types.h"
s32 func_08000860_71C2E0();                         /* extern */
extern char func_8003521C_35E1C;
extern char func_8021BB04_5D6FD4;
extern char func_80224D50_5E0220;
extern M2C_UNK func_08000AB0_71C530;

void func_08000EE0_71C960(void *arg0, M2C_UNK arg1) {
    if (func_08000860_71C2E0() == 0) {
        if (M2C_FIELD(arg0, u16 *, 0x94) & 1) {
            M2C_FIELD(arg0, f32 *, 0x7C) = 2.0f;
        }
        ((M2C_UNK (*)(void *, M2C_UNK))&func_80224D50_5E0220)(arg0, 2);
        if (((s32 (*)(void *, f32, f32, M2C_UNK))&func_8021BB04_5D6FD4)(arg0, (f32) M2C_FIELD(arg0, s16 *, 0xD8), (f32) M2C_FIELD(arg0, s16 *, 0xDA), 0x40400000) == 0) {
            ((M2C_UNK (*)(M2C_UNK *))&func_8003521C_35E1C)(&func_08000AB0_71C530);
            M2C_FIELD(arg0, s32 *, 0xD8) = 0;
        }
    }
}
