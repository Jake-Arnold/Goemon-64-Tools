#include "m2c_types.h"

typedef struct {
    u8 pad0[0x30];
    u8 unk30;
} Arg0_1F68B4;

typedef struct {
    u8 pad0[0x28];
    f32 unk28;
} Arg1_1F68B4;

extern f32 func_8001B13C_1BD3C(Arg1_1F68B4 *);
void func_801E019C_59C16C(Arg0_1F68B4 *, s32);
void func_801FBECC_5B7E9C(Arg0_1F68B4 *);

void func_801FB798_5B7768(Arg0_1F68B4 *arg0, Arg1_1F68B4 *arg1) {
    arg0->unk30 &= ~1;
    if ((((f32 (*)(Arg1_1F68B4 *))func_8001B13C_1BD3C)(arg1) - 1.0f) <= arg1->unk28) {
        func_801FBECC_5B7E9C(arg0);
        func_801E019C_59C16C(arg0, 0xAE);
    }
}
