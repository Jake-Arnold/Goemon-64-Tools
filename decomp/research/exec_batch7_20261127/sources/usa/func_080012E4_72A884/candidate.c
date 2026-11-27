#include "m2c_types.h"

typedef struct Struct_080012E4_Sub Struct_080012E4_Sub;

struct Struct_080012E4_Sub {
    Struct_080012E4_Sub *unk0;
    u8 pad4[0x10];
    s16 unk14;
    s16 unk16;
    s16 unk18;
};

typedef struct {
    u8 pad0[0x18];
    Struct_080012E4_Sub *unk18;
} Struct_080012E4;

void func_080012E4_72A884(Struct_080012E4 *arg0, s32 arg1, s32 arg2, s32 arg3) {
    Struct_080012E4_Sub *sub;

    sub = arg0->unk18;
    sub->unk14 = arg1;
    sub->unk16 = arg2;
    sub->unk18 = arg3;
    sub = sub->unk0;
    sub->unk14 = (arg1 + 0x200) & 0x3FF;
    sub->unk16 = arg2;
    sub->unk18 = arg3;
}
