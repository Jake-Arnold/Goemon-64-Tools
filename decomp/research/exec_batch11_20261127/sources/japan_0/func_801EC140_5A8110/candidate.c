#include "m2c_types.h"
void func_80033510_34110(u16, u16, u16, f32 *, f32 *, f32 *); /* extern */
void func_801EC4E8_5A84B8(s32, s32);                /* extern */
extern s32 D_80201534_5BD504;

typedef struct {
    u8 pad0[8];
    f32 x;
    f32 y;
    f32 z;
    u16 rx;
    u16 ry;
    u16 rz;
} Unk18;

typedef struct {
    u8 pad0[0x18];
    Unk18 *unk18;
} Arg0;

void func_801EC140_5A8110(Arg0 *arg0) {
    Unk18 *unk18 = arg0->unk18;
    f32 x = 0.0f;
    f32 y = 6.0f;
    f32 z = 7.5f;

    func_80033510_34110(unk18->rx, unk18->ry, unk18->rz, &x, &y, &z);
    unk18->x += x;
    unk18->y += y;
    unk18->z += z;
    func_801EC4E8_5A84B8(D_80201534_5BD504, 0x10);
}
