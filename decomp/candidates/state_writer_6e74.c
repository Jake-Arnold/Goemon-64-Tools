#include "common.h"

extern u8 D_800BCCC0_BD8C0[];

void func_80006274_6E74(s32 arg0, s32 arg1) {
    volatile s32 arg0_home = arg0;
    volatile u8 *base = D_800BCCC0_BD8C0 + 0x7FFF;
    *(volatile u16 *)(base + 0x2DB7) = 1;
    *(volatile u16 *)(base + 0x2E3B) = (u16)arg0;
    *(volatile unsigned int *)(base + 0x2E3D) = (unsigned int)arg1;
}
