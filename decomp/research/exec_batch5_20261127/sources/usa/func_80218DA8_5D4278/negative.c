#include "m2c_types.h"

typedef struct {
    u8 pad[0x48];
    s32 unk48;
    u8 pad2[2];
    s16 unk4E;
    s16 unk50;
    s16 unk52;
} Unk5D4278;

void func_80218DA8_5D4278(Unk5D4278 *arg0, s32 arg1, s32 arg2, s32 arg3) {
    arg0->unk48 = -1;
    arg0->unk4E = arg1 / 10;
    arg0->unk50 = arg2;
    arg0->unk52 = arg3;

    *(volatile s32 *)0x80000000 = 1;
}
