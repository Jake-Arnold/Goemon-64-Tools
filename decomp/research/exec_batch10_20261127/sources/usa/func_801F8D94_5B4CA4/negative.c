#include "m2c_types.h"
typedef struct {
    u8 pad0[0xADB6];
    s16 unkADB6;
    u8 padADB8[0x12];
    s8 unkADCA;
    u8 padADCB[0x55];
    s8 unkAE20;
    s8 unkAE21[2];
    s8 unkAE23;
    s8 unkAE24[5];
    s8 unkAE29;
    u8 padAE2A[0x1F3];
    s8 unkB01D;
} UnkBCCC0;

typedef struct {
    u8 pad0[0xF88D];
    s8 unkF88D;
    u8 padF88E[6];
    s32 unkF894;
    s8 unkF898;
} Unk14CCC0;

extern UnkBCCC0 D_800BCCC0_BD8C0;
extern Unk14CCC0 D_8014CCC0_14D8C0;

void func_801F8D94_5B4CA4(void) {
    D_8014CCC0_14D8C0.unkF88D = 0;
    D_800BCCC0_BD8C0.unkAE29 = 0;
    D_8014CCC0_14D8C0.unkF898 = 0;
    D_8014CCC0_14D8C0.unkF894 = 0;
    D_800BCCC0_BD8C0.unkAE23 = 0;
    D_800BCCC0_BD8C0.unkAE20 = 0;
    D_800BCCC0_BD8C0.unkB01D = 7;
    D_800BCCC0_BD8C0.unkADCA = 2;
    D_800BCCC0_BD8C0.unkADB6 = 0;

    *(volatile s32 *)0x80000000 = 1;
}
