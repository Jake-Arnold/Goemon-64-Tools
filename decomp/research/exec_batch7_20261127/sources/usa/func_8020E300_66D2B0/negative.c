#include "m2c_types.h"

extern f32 D_80216BD0_675B80[];

typedef struct {
    u8 pad0[0x5C];
    f32 unk5C;
    f32 unk60;
    f32 unk64;
} Struct_8020E300;

void func_8020E300_66D2B0(Struct_8020E300 *arg0, f32 arg1, s32 arg2, f32 arg3) {
    arg0->unk5C = arg1;
    arg0->unk60 = D_80216BD0_675B80[arg2];
    arg0->unk64 = arg3;

    *(volatile s32 *)0x80000000 = 1;
}
