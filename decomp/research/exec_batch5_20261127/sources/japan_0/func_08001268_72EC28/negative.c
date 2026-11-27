#include "m2c_types.h"

typedef struct UnkStruct12AC {
    struct UnkStruct12AC *unk0;
    s32 unk4;
    f32 unk8;
    f32 unkC;
    f32 unk10;
} UnkStruct12AC;

typedef struct {
    u8 pad0[0x18];
    UnkStruct12AC *unk18;
} Arg0Struct12AC;

void func_08001268_72EC28(Arg0Struct12AC *arg0, f32 arg1, f32 arg2, f32 arg3) {
    UnkStruct12AC *ptr;

    ptr = arg0->unk18;
    ptr->unk8 = arg1;
    ptr->unkC = arg2;
    ptr->unk10 = arg3;
    ptr = ptr->unk0;
    ptr->unk8 = arg1;
    ptr->unkC = arg2;
    ptr->unk10 = arg3;

    *(volatile s32 *)0x80000000 = 1;
}
