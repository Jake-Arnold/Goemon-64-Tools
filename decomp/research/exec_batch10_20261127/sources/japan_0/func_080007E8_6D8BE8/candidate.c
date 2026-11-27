#include "m2c_types.h"
extern M2C_UNK func_8021FE0C_5DB39C;

typedef struct {
    u8 unk_00[0x68];
    s32 unk_68;
    u8 unk_6C[0x9];
    s8 unk_75;
    u8 unk_76[0x25];
    s8 unk_9B;
} Obj0_080007E8;

typedef struct {
    u8 unk_00[0x14];
    u16 unk_14;
} Obj1_080007E8;

void func_080007E8_6D8BE8(Obj0_080007E8 *arg0, Obj1_080007E8 *arg1) {
    if (arg1->unk_14 != 0) {
        arg1->unk_14 += 0x20;
    } else {
        arg0->unk_9B = 0;
    }
    if (!(arg0->unk_68 & 0x20)) {
        arg0->unk_68 &= ~1;
        arg0->unk_75 = 0x19;
        arg1->unk_14 = 0;
        ((void (*)(Obj0_080007E8 *, s32, s32, Obj1_080007E8 *))&func_8021FE0C_5DB39C)(arg0, 0, 1, arg1);
    }
}
