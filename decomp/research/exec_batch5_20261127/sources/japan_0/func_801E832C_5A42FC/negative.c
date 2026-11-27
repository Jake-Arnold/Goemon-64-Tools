#include "m2c_types.h"

typedef struct {
    u8 pad0[0x64];
    u8 unk64;
} Unk59EFF4_18;

typedef struct {
    u8 pad0[0x04];
    f32 unk04;
    u8 pad1[0x28];
    s16 unk30;
    u8 pad2[0x16];
    f32 unk48;
} Unk59EFF4_5C;

typedef struct {
    u8 pad0[0x18];
    Unk59EFF4_18 *unk18;
    u8 pad1[0x14];
    u8 unk30;
    u8 pad2[0x2B];
    Unk59EFF4_5C *unk5C;
    u8 pad3[0x08];
    f32 unk68;
    f32 unk6C;
    f32 unk70;
    u8 pad4[0x30];
    f32 unkA4;
    u8 pad5[0x2C];
    u8 unkD4;
} Unk59EFF4;

extern f32 D_802101BC_5CC18C;

void func_801E832C_5A42FC(Unk59EFF4 *arg0) {
    Unk59EFF4_18 *temp_18;

    temp_18 = arg0->unk18;
    arg0->unk30 &= ~1;
    arg0->unk5C->unk30 = 0;
    arg0->unkD4 = 0;
    temp_18->unk64 = 0;
    arg0->unkA4 = 0.0f;
    arg0->unk5C->unk04 = 0.0f;
    arg0->unk68 = 0.0f;
    arg0->unk6C = 0.0f;
    arg0->unk70 = 0.0f;
    arg0->unk5C->unk48 = D_802101BC_5CC18C;

    *(volatile s32 *)0x80000000 = 1;
}
