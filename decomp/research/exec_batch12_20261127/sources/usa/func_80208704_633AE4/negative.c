#include "m2c_types.h"

void func_8003521C_35E1C(void *);
s32 func_8003767C_3827C(void);
void func_80038BC8_397C8(s32);
s32 func_801D5064_600444(f32, s32, s32);
extern u8 D_3ADE4[];
extern s32 D_8015C5C8_15D1C8;
extern void func_8020878C_633B6C(void);
extern void func_80208898_633C78(void);

void func_80208704_633AE4(s32 arg0, M2C_UNK arg1) {
    if ((func_8003767C_3827C() != 0) && (D_3ADE4[D_8015C5C8_15D1C8] == 5)) {
        func_80038BC8_397C8(0x38);
        func_8003521C_35E1C(func_80208898_633C78);
        return;
    }
    if (func_801D5064_600444(1.0f, 0x36, 0xB8) != 0) {
        func_8003521C_35E1C(func_8020878C_633B6C);
    }

    *(volatile int *)0x80000000 = 1;
}
