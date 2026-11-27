#include "m2c_types.h"

typedef struct {
    u8 pad0[0x8A];
    u16 unk8A;
    u8 pad8C[0x45];
    u8 unkD1;
    u8 padD2[0x2];
    s16 unkD4;
} Arg0;

typedef struct {
    u8 pad0[0x14];
    s16 unk14;
} Arg1;

void func_80034E8C_35A8C(void *);
extern u8 func_08000CCC_70049C[];

void func_08000C80_700450(Arg0 *arg0, Arg1 *arg1) {
    void (*fn)(void *);

    if (--arg0->unk8A == 0) {
        arg1->unk14 = 0;
        arg0->unkD4 = arg0->unkD1;
        fn = func_80034E8C_35A8C;
        fn(func_08000CCC_70049C);
    }
}
