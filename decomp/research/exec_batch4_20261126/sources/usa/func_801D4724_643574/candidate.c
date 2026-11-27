#include "m2c_types.h"
s16 func_800040A8_4CA8(f32, f32);
extern f32 D_801EF0E0_65DF30;

typedef struct {
    u8 pad0[0x5C];
    f32 unk5C;
    u8 pad60[4];
    f32 unk64;
    u8 pad68[0xA4 - 0x68];
    s32 unkA4;
    u8 padA8[4];
    s32 unkAC;
} Struct801D4724_0;

typedef struct {
    u8 pad0[0x18];
    s16 unk18;
} Struct801D4724_1;

void func_801D4724_643574(Struct801D4724_0 *arg0, Struct801D4724_1 *arg1) {
    s32 temp_v0;

    temp_v0 = arg0->unkA4;
    arg0->unk64 += 28.0;
    arg0->unk5C += (f32) temp_v0 / 1000.0f;
    temp_v0 += arg0->unkAC;
    arg0->unkA4 = temp_v0;
    arg1->unk18 = func_800040A8_4CA8((f32) -temp_v0, D_801EF0E0_65DF30);
}
