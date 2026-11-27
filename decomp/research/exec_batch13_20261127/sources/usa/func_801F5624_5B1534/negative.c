#include "m2c_types.h"

typedef struct {
    u8 pad0[0x28];
    f32 unk28;
} Sub_1F5624;

typedef struct {
    u8 pad0[0x18];
    Sub_1F5624 *unk18;
    u8 pad1C[0x14];
    u8 unk30;
    u8 pad31[0x1B];
    u8 unk4C;
    u8 pad4D[0xF];
    s16 *unk5C;
} Arg0_1F5624;

extern u8 func_8001B5AC_1C1AC[];
void func_801DACDC_596BEC(Arg0_1F5624 *, u8);

void func_801F5624_5B1534(Arg0_1F5624 *arg0, u8 arg1) {
    Sub_1F5624 *s = arg0->unk18;

    arg0->unk30 &= ~1;
    if ((((f32 (*)(Sub_1F5624 *))func_8001B5AC_1C1AC)(s) - 1.0f) <= s->unk28) {
        arg0->unk30 |= 1;
        *arg0->unk5C = 0;
        arg0->unk4C = 0x14;
        func_801DACDC_596BEC(arg0, arg1);
    }

    *(volatile int *)0x80000000 = 1;
}
