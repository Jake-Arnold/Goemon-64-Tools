#include "m2c_types.h"

void func_8003521C_35E1C(void *);
void func_800369F0_375F0(s32);
void func_801F9BA8_5B5AB8(void);
extern u8 D_3AFE0[];
extern s8 D_8015C562_15D162;
extern s32 D_8015C5C8_15D1C8;
extern u8 func_801F7B0C_5B3A1C[];

void func_801F7AA4_5B39B4(s32 arg0, s32 arg1) {
    u16 temp_v0;

    D_8015C562_15D162 = 1;
    func_800369F0_375F0(arg0);
    temp_v0 = *(u16 *)(D_3AFE0 + D_8015C5C8_15D1C8);
    if ((s32)temp_v0 < 0x23A || (s32)temp_v0 >= 0x23C) {
        func_801F9BA8_5B5AB8();
    }
    func_8003521C_35E1C(func_801F7B0C_5B3A1C);

    *(volatile int *)0x80000000 = 1;
}
