#include "m2c_types.h"

typedef struct {
    u8 pad0[0xC];
    f32 unkC;
} UnkTbl;

typedef struct {
    s16 unk0;
    s16 unk2;
    f32 unk4;
    u8 pad8[0x28];
    s16 unk30;
    s16 unk32;
} Unk5C;

typedef struct {
    u8 pad0[0x5C];
    Unk5C *unk5C;
    u8 pad60[0x8];
    f32 unk68;
    f32 unk6C;
    f32 unk70;
    u8 pad74[0x1C];
    u8 unk90;
    u8 pad91[0x13];
    f32 unkA4;
    u8 padA8[0x3C];
    f32 unkE4;
    f32 unkE8;
} Arg0;

void func_801DACDC_596BEC(Arg0 *, s32);
s32 func_801E7DE8_5A3CF8(void);
extern UnkTbl *D_801FC60C_5B851C[];
extern f32 D_8020AF2C_5C6E3C;

void func_801DA84C_59675C(Arg0 *arg0, s16 arg1) {
    arg0->unk5C->unk0 = 0;
    arg0->unk70 = 0.0f;
    arg0->unk6C = 0.0f;
    arg0->unk68 = 0.0f;
    arg0->unk5C->unk4 = 1.0f;
    arg0->unkE8 = 1.0f;
    arg0->unkE4 = 1.0f;
    if (func_801E7DE8_5A3CF8() != 0) {
        arg0->unkA4 = D_8020AF2C_5C6E3C;
    } else {
        arg0->unkA4 = 3.0f;
    }
    arg0->unk5C->unk2 = ((arg1 + 0x200) & 0x3FF) | 0x400;
    func_801DACDC_596BEC(arg0, 0x1D);
    arg0->unk5C->unk32 = (s16)(s32)D_801FC60C_5B851C[arg0->unk90]->unkC;
    arg0->unk5C->unk30 = 0;

    *(volatile s32 *)0x80000000 = 1;
}
