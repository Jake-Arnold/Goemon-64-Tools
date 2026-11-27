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

M2C_UNK func_8003C4D0_3D0D0(Struct3D220 **);
extern Struct3D220 *D_80178E00_179A00;

void func_8003C290_3CE90(void) {
    if (D_80178E00_179A00->unk8C == 0) {
        if (D_80178E00_179A00->unk7C != 0) {
            D_80178E00_179A00->unk7C--;
        } else {
            D_80178E00_179A00->unk6 |= 2;
            D_80178E00_179A00->unk7D--;
            if (D_80178E00_179A00->unk7D != 0) {
                D_80178E00_179A00->unk28 += D_80178E00_179A00->unk84;
            } else {
                D_80178E00_179A00->unk28 = D_80178E00_179A00->unk80;
            }
        }
    } else {
        func_8003C4D0_3D0D0(&D_80178E00_179A00);
    }

    *(volatile s32 *)0x80000000 = 1;
}
