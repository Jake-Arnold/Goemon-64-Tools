#include "m2c_types.h"

typedef struct {
    u8 pad0[0x48];
    s32 unk48;
    u8 pad4C[0x10];
    s16 *unk5C;
} Arg0_1F5EB8;

typedef struct {
    u8 pad0[0x28];
    f32 unk28;
} Arg1_1F5EB8;

extern u8 func_8001B13C_1BD3C[];
void func_801E019C_59C16C(Arg0_1F5EB8 *, s32);

void func_801FAEA8_5B6E78(Arg0_1F5EB8 *arg0, Arg1_1F5EB8 *arg1) {
    if ((((f32 (*)(Arg1_1F5EB8 *))func_8001B13C_1BD3C)(arg1) - 1.0f) <= arg1->unk28) {
        arg0->unk48 = 0;
        *arg0->unk5C = 0;
        func_801E019C_59C16C(arg0, 0);
    }

    *(volatile int *)0x80000000 = 1;
}
