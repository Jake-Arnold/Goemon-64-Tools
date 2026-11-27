#include "m2c_types.h"

typedef struct {
    u8 pad0[6];
    u8 unk6;
    u8 pad7[0x28 - 7];
    s32 unk28;
    u8 pad2C[0x7C - 0x2C];
    u8 unk7C;
    u8 unk7D;
    u8 pad7E[2];
    s32 unk80;
    s32 unk84;
    u8 pad88[4];
    u8 unk8C;
} Struct3D220;

M2C_UNK func_8003C860_3D460(Struct3D220 **);
extern Struct3D220 *D_801C1728_1C2328;

void func_8003C620_3D220(void) {
    if (D_801C1728_1C2328->unk8C == 0) {
        if (D_801C1728_1C2328->unk7C != 0) {
            D_801C1728_1C2328->unk7C--;
        } else {
            D_801C1728_1C2328->unk6 |= 2;
            D_801C1728_1C2328->unk7D--;
            if (D_801C1728_1C2328->unk7D != 0) {
                D_801C1728_1C2328->unk28 += D_801C1728_1C2328->unk84;
            } else {
                D_801C1728_1C2328->unk28 = D_801C1728_1C2328->unk80;
            }
        }
    } else {
        func_8003C860_3D460(&D_801C1728_1C2328);
    }

    *(volatile s32 *)0x80000000 = 1;
}
