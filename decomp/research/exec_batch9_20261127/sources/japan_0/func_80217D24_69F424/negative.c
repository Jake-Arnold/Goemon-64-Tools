#include "m2c_types.h"
typedef struct {
    u8 pad0[0x5];
    s8 unk5;
    u8 pad6[0x6];
    s16 unkC;
    u16 unkE;
    s16 unk10;
    s16 unk12;
    f32 unk14;
    f32 unk18;
    f32 unk1C;
    f32 unk20;
    f32 unk24;
    f32 unk28;
} UnkSub2;

typedef struct {
    u8 pad0[0x10];
    f32 unk10;
    u8 pad14[0xC];
    f32 unk20;
    u8 pad24[0x8];
    UnkSub2 *unk2C;
} UnkSub1;

typedef struct {
    u8 pad0[0x5C];
    UnkSub1 unk5C;
} UnkObj;

UnkObj *func_80034A78_35678(s32, void (*)(void), s32);
UnkSub2 *func_80035B5C_3675C(UnkObj *, s32, s32);
extern f32 D_80219F74_6A1674;
void func_80217CB4_69F3B4(void);

UnkObj *func_80217D24_69F424(s32 arg0) {
    UnkObj *temp_v0;
    UnkSub1 *temp_v1;

    temp_v0 = func_80034A78_35678(arg0, func_80217CB4_69F3B4, 0);
    if (temp_v0 == NULL) {
        { *(volatile s32 *)0x80000000 = 1; } return NULL;
    }
    temp_v1 = &temp_v0->unk5C;
    if ((temp_v1->unk2C = func_80035B5C_3675C(temp_v0, 5, 1)) == NULL) {
        return NULL;
    }
    temp_v1->unk2C->unkE = 0x8009;
    temp_v1->unk10 = 0.0f;
    temp_v1->unk2C->unk14 = 0.0f;
    temp_v1->unk20 = 0.0f;
    temp_v1->unk2C->unk18 = 0.0f;
    temp_v1->unk2C->unkC = 0x7B;
    temp_v1->unk2C->unk5 = 1;
    temp_v1->unk2C->unk10 = 0x280;
    temp_v1->unk2C->unk12 = 0xF0;
    temp_v1->unk2C->unk24 = D_80219F74_6A1674;
    temp_v1->unk2C->unk28 = 239.0f;
    return temp_v0;
}
