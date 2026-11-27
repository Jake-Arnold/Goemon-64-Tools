#include "m2c_types.h"

typedef struct {
    u8 unk0[8];
    f32 unk8;
    f32 unkC;
    f32 unk10;
} VecStruct;

extern VecStruct *D_8020151C_5BD4EC;
extern VecStruct *D_80201524_5BD4F4;
extern VecStruct *D_8020152C_5BD4FC;

void func_08000A2C_73D4AC(s32 arg0, f32 arg1, f32 arg2, f32 arg3) {
    D_8020152C_5BD4FC->unk8 = D_80201524_5BD4F4->unk8 = D_8020151C_5BD4EC->unk8 = arg1;
    D_8020152C_5BD4FC->unkC = D_80201524_5BD4F4->unkC = D_8020151C_5BD4EC->unkC = arg2;
    D_8020152C_5BD4FC->unk10 = D_80201524_5BD4F4->unk10 = D_8020151C_5BD4EC->unk10 = arg3;

    *(volatile s32 *)0x80000000 = 1;
}
