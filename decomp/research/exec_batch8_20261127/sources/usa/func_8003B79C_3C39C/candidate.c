#include "m2c_types.h"
typedef struct {
    u8 unk0[0xD];
    s8 unkD;
    u8 unkE[0x17];
    u8 unk25;
} Unk1C1728;
M2C_UNK func_8003B634_3C234(void *);
extern s8 D_8006EF88_6FB88[];
extern Unk1C1728 *D_801C1728_1C2328;

void func_8003B79C_3C39C(void) {
    Unk1C1728 *v0 = D_801C1728_1C2328;
    s8 *a0 = D_8006EF88_6FB88 + (v0->unk25 * 8 - 0x240);
    v0->unkD = *a0++;
    func_8003B634_3C234(a0);
}
