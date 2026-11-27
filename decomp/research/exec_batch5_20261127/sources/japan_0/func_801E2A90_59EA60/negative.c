#include "m2c_types.h"

typedef struct {
    u8 pad[0x60];
    u8 unk60;
} Unk5995F0;

void func_80038838_39438(u16);
extern u16 D_80208F50_5C4F20[][4];

void func_801E2A90_59EA60(Unk5995F0 *arg0, u16 arg1) {
    func_80038838_39438(D_80208F50_5C4F20[arg1][arg0->unk60]);

    *(volatile s32 *)0x80000000 = 1;
}
