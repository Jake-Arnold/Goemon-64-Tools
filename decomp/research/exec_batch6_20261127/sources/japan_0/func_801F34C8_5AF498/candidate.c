#include "m2c_types.h"

typedef struct UnkEE4AC {
    u8 pad0[0x5C];
    s32 unk5C;
    u8 unk60;
    u8 unk61;
    s16 unk62;
    u8 unk64;
    u8 unk65;
    u8 unk66;
    u8 unk67;
    s16 unk68;
    u8 pad6A[0x1A];
    struct UnkEE4AC *unk84;
} UnkEE4AC;

void func_801F34C8_5AF498(UnkEE4AC *arg0, UnkEE4AC *arg1, u8 arg2) {
    arg0->unk5C = arg1->unk5C;
    arg0->unk60 = 0;
    arg0->unk61 = 0;
    arg0->unk62 = 0;
    arg0->unk64 = arg2;
    arg0->unk65 = 0;
    arg0->unk66 = 0;
    arg0->unk84 = arg1;
    arg0->unk67 = 0;
    arg0->unk68 = 0;
}
