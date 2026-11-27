#include "m2c_types.h"

typedef struct {
    u8 pad0[0x61];
    u8 unk61;
    u8 pad62[3];
    u8 unk65;
} Arg0_1E95BC;

typedef struct {
    u8 pad0[0x28];
    f32 unk28;
    s32 unk2C;
} Arg1_1E95BC;

extern u8 func_8001B5AC_1C1AC[];
void func_801E99CC_5A58DC(Arg0_1E95BC *, Arg1_1E95BC *, s32);

void func_801E95BC_5A54CC(Arg0_1E95BC *arg0, Arg1_1E95BC *arg1) {
    f32 temp;

    func_801E99CC_5A58DC(arg0, arg1, 1);
    temp = arg1->unk28 + 1.5f;
    arg1->unk28 = temp;
    if ((((f32 (*)(Arg1_1E95BC *))func_8001B5AC_1C1AC)(arg1) - 1.0f) <= temp) {
        arg1->unk2C = 0;
        if (arg0->unk61 == 0) {
            arg0->unk65 = 1;
        }
    }

    *(volatile int *)0x80000000 = 1;
}
