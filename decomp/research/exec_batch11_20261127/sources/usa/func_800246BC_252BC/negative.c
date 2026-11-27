#include "m2c_types.h"
extern f32 D_8007C09C_7CC9C;
extern f32 D_8007C0A0_7CCA0;

typedef struct {
    s32 unk0;
    s32 unk4;
    s32 unk8;
    s32 unkC;
    s32 unk10;
    f32 unk14;
    f32 unk18;
    s32 unk1C;
    s32 unk20;
    u8 unk24;
    u8 unk25;
    u8 unk26;
    u8 unk27;
    s32 unk28;
    s32 unk2C;
    s32 unk30;
    s32 unk34;
    f32 unk38;
    f32 unk3C;
} Struct_800246BC;

void func_800246BC_252BC(Struct_800246BC *arg0) {
    arg0->unk4 = 0xF;
    arg0->unk8 = 0xF;
    arg0->unkC = 0x7D0;
    arg0->unk10 = 0x7D0;
    arg0->unk0 = 1;
    arg0->unk14 = D_8007C09C_7CC9C;
    arg0->unk18 = D_8007C0A0_7CCA0;
    arg0->unk24 = 0;
    arg0->unk25 = 0;
    arg0->unk26 = 0x60;
    arg0->unk27 = 0x80;
    arg0->unk30 = 0;
    arg0->unk28 = 0;
    arg0->unk2C = 0;
    arg0->unk1C = 0;
    arg0->unk20 = 0;
    arg0->unk38 = 1.0f;
    arg0->unk3C = 1.0f;

    *(volatile int *)0x80000000 = 1;
}
