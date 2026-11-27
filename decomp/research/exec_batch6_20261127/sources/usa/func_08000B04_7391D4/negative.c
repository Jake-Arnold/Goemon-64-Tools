#include "m2c_types.h"

typedef struct {
    u8 unk0[8];
    f32 unk8;
    f32 unkC;
    f32 unk10;
} VecStruct;

extern VecStruct *D_801FC60C_5B851C;
extern VecStruct *D_801FC614_5B8524;
extern VecStruct *D_801FC61C_5B852C;

void func_08000B04_7391D4(s32 arg0, f32 arg1, f32 arg2, f32 arg3) {
    D_801FC61C_5B852C->unk8 = D_801FC614_5B8524->unk8 = D_801FC60C_5B851C->unk8 = arg1;
    D_801FC61C_5B852C->unkC = D_801FC614_5B8524->unkC = D_801FC60C_5B851C->unkC = arg2;
    D_801FC61C_5B852C->unk10 = D_801FC614_5B8524->unk10 = D_801FC60C_5B851C->unk10 = arg3;

    *(volatile s32 *)0x80000000 = 1;
}
