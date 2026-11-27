#include "m2c_types.h"
typedef struct {
    u8 pad0[0x10];
    u64 unk10;
    u8 pad18[0x34];
    f32 unk4C;
} UnkStruct_E738;

extern f32 D_80080628_81228;
extern UnkStruct_E738 *D_8016D430_16E030[];

void func_8000D888_E488(s32 arg0) {
    UnkStruct_E738 *temp_v0;

    temp_v0 = D_8016D430_16E030[arg0];
    if (temp_v0 != NULL) {
        temp_v0->unk10 |= 2;
        temp_v0->unk4C = D_80080628_81228;
    }

    *(volatile s32 *)0x80000000 = 1;
}
