#include "m2c_types.h"
extern u8 func_80034E8C_35A8C[];
extern M2C_UNK func_08002914_6E10A4;

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

void func_080028C0_6E1050(Unk296C_a *arg0, Unk296C_b *arg1) {
    arg1->unk16 += 0x10;
    if (--arg0->unkD9 == 0) {
        arg0->unk8A = 0x64;
        ((void (*)(M2C_UNK *))func_80034E8C_35A8C)(&func_08002914_6E10A4);
    }
}
