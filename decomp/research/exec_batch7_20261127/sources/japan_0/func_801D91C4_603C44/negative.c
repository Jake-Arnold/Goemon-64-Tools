#include "m2c_types.h"
typedef struct {
    u8 pad0[0x29C];
    s32 unk29C;
    s32 unk2A0;
} UnkGlobal_D3AA4;

extern UnkGlobal_D3AA4 D_80161DF8_1629F8;

void func_801D91C4_603C44(void) {
    D_80161DF8_1629F8.unk29C += 0x64;
    D_80161DF8_1629F8.unk2A0 += 0x64;
    if (D_80161DF8_1629F8.unk29C >= 0x3E7) {
        D_80161DF8_1629F8.unk29C = 0x3E7;
    }
    if (D_80161DF8_1629F8.unk2A0 >= 0x3E7) {
        D_80161DF8_1629F8.unk2A0 = 0x3E7;
    }

    *(volatile s32 *)0x80000000 = 1;
}
