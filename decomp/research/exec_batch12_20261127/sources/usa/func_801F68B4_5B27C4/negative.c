#include "m2c_types.h"

typedef struct {
    u8 pad0[0x30];
    u8 unk30;
} Arg0_1F68B4;

typedef struct {
    u8 pad0[0x28];
    f32 unk28;
} Arg1_1F68B4;

extern f32 func_8001B5AC_1C1AC(Arg1_1F68B4 *);
void func_801DACDC_596BEC(Arg0_1F68B4 *, s32);
void func_801F6FE8_5B2EF8(Arg0_1F68B4 *);

void func_801F68B4_5B27C4(Arg0_1F68B4 *arg0, Arg1_1F68B4 *arg1) {
    arg0->unk30 &= ~1;
    if ((((f32 (*)(Arg1_1F68B4 *))func_8001B5AC_1C1AC)(arg1) - 1.0f) <= arg1->unk28) {
        func_801F6FE8_5B2EF8(arg0);
        func_801DACDC_596BEC(arg0, 0xAE);
    }

    *(volatile int *)0x80000000 = 1;
}
