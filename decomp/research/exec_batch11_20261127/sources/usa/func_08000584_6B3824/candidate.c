#include "m2c_types.h"

typedef struct {
    u8 pad0[0x5E];
    s16 unk5E;
    s32 unk60;
} Unk0584_0;

typedef struct {
    u8 pad0[0x1C];
    f32 unk1C;
    f32 unk20;
    f32 unk24;
} Unk0584_1;

extern u8 func_8003521C_35E1C[];
extern u8 func_80216E1C_5D22EC[];
extern u8 func_0800056C_6B380C[];

void func_08000584_6B3824(Unk0584_0 *arg0, Unk0584_1 *arg1) {
    arg0->unk5E = 0x7E;
    arg0->unk60 = 0x4006E0;
    ((void (*)(Unk0584_0 *, s32, Unk0584_1 *))func_80216E1C_5D22EC)(arg0, 1, arg1);
    arg1->unk24 = 1.0f;
    arg1->unk20 = 1.0f;
    arg1->unk1C = 1.0f;
    ((void (*)(u8 *))func_8003521C_35E1C)(func_0800056C_6B380C);
}
