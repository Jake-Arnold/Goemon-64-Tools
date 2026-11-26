#include "m2c_types.h"
typedef struct {
    s16 unk0;
    s16 unk2;
    s16 unk4;
    s16 unk6;
    s16 unk8;
    u8 unkA[0xE];
} Unk5DE53C;
extern Unk5DE53C D_8023B3A0_5F6870[];

void func_8022306C_5DE53C(s32 arg0) {
    Unk5DE53C *temp_v0 = &D_8023B3A0_5F6870[arg0];

    temp_v0->unk8 = 0;
    temp_v0->unk2 = 0;
    temp_v0->unk4 = 0;
    temp_v0->unk6 = temp_v0->unk8;
}
