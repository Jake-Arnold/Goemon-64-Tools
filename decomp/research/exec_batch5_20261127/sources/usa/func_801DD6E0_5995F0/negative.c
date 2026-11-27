#include "m2c_types.h"

typedef struct {
    u8 pad[0x60];
    u8 unk60;
} Unk5995F0;

void func_80038BC8_397C8(u16);
extern u16 D_80204060_5BFF70[][4];

void func_801DD6E0_5995F0(Unk5995F0 *arg0, u16 arg1) {
    func_80038BC8_397C8(D_80204060_5BFF70[arg1][arg0->unk60]);

    *(volatile s32 *)0x80000000 = 1;
}
