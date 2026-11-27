#include "m2c_types.h"
typedef struct {
    u8 unk0[0xD];
    s8 unkD;
    u8 unkE[0x17];
    u8 unk25;
} Unk1C1728;
M2C_UNK func_8003B2A4_3BEA4(void *);
extern s8 D_80074A68_75668[];
extern Unk1C1728 *D_80178E00_179A00;

void func_8003B40C_3C00C(void) {
    Unk1C1728 *v0 = D_80178E00_179A00;
    s8 *a0 = D_80074A68_75668 + (v0->unk25 * 8 - 0x240);
    v0->unkD = *a0++;
    func_8003B2A4_3BEA4(a0);
}
