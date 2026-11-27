#include "m2c_types.h"
void func_8003521C_35E1C(M2C_UNK *);
void func_80038BC8_397C8(s32, void *);
extern f64 D_8020E890_639C70;

typedef struct {
    u8 pad0[8];
    f32 unk8;
} UnkA1;

typedef struct {
    u8 pad0[0xC];
    f32 unkC;
} UnkA0;

typedef struct {
    u8 pad0[0x18];
    UnkA1 *unk18;
} Unk1D8;

typedef struct {
    u8 pad0[0xA0];
    UnkA0 unkA0;
    u8 padB0[0x1D8 - 0xB0];
    Unk1D8 *unk1D8;
    u8 pad1DC[0x2C1 - 0x1DC];
    s8 unk2C1;
} GlobalEED0;

typedef struct {
    u8 pad0[0x7C];
    s32 unk7C;
} Arg0;

extern GlobalEED0 *D_8020EED0_63A2B0;
extern M2C_UNK func_801F9860_624C40;

void func_801F977C_624B5C(Arg0 *arg0, M2C_UNK arg1) {
    UnkA0 *temp_v0;
    UnkA1 *temp_a1;

    temp_v0 = &D_8020EED0_63A2B0->unkA0;
    temp_a1 = D_8020EED0_63A2B0->unk1D8->unk18;
    temp_v0->unkC = (f32) ((f64) temp_v0->unkC + 0.5);
    if (D_8020E890_639C70 == (f64) temp_v0->unkC) {
        func_80038BC8_397C8(0x27F, temp_a1);
    }
    if (temp_v0->unkC >= 150.0f) {
        D_8020EED0_63A2B0->unk2C1 = 1;
    }
    if (temp_a1->unk8 <= temp_v0->unkC) {
        arg0->unk7C = 0xC8;
        func_8003521C_35E1C(&func_801F9860_624C40);
    }

    *(volatile int *)0x80000000 = 1;
}
