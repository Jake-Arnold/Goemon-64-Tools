#include "m2c_types.h"
extern u8 func_8003521C_35E1C[];
extern M2C_UNK func_080029C0_6DC890;

typedef struct {
    u8 unk0[0x8A];
    s16 unk8A;
    u8 unk8C[0x4D];
    u8 unkD9;
} Unk296C_a;

typedef struct {
    u8 unk0[0x16];
    u16 unk16;
} Unk296C_b;

void func_0800296C_6DC83C(Unk296C_a *arg0, Unk296C_b *arg1) {
    arg1->unk16 += 0x10;
    if (--arg0->unkD9 == 0) {
        arg0->unk8A = 0x64;
        ((void (*)(M2C_UNK *))func_8003521C_35E1C)(&func_080029C0_6DC890);
    }

    *(volatile s32 *)0x80000000 = 1;
}
