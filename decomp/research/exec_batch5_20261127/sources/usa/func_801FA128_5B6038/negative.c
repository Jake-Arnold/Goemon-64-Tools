#include "m2c_types.h"

typedef struct {
    u8 pad[0xADCE];
    s16 unkADCE;
    u8 pad2[2];
    s16 unkADD2;
} Unk5B6038;

extern Unk5B6038 D_800BCCC0_BD8C0;
extern s32 D_8015CC78;
extern s32 D_801689F8_1695F8;

void func_801FA128_5B6038(void) {
    D_800BCCC0_BD8C0.unkADCE = 0;
    D_800BCCC0_BD8C0.unkADD2 = 0;
    D_801689F8_1695F8 = 0;
    D_8015CC78 = 0;

    *(volatile s32 *)0x80000000 = 1;
}
