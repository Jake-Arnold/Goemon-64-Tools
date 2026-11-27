#include "m2c_types.h"
void func_80033898_34498(u16, u16, u16, f32 *, f32 *, f32 *); /* extern */
void func_801E7398_5A32A8(s32, s32);                /* extern */
extern s32 D_801FC624_5B8534;

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

void func_801E6FE0_5A2EF0(Arg0 *arg0) {
    Unk18 *unk18 = arg0->unk18;
    f32 x = 0.0f;
    f32 y = 6.0f;
    f32 z = 7.5f;

    func_80033898_34498(unk18->rx, unk18->ry, unk18->rz, &x, &y, &z);
    unk18->x += x;
    unk18->y += y;
    unk18->z += z;
    func_801E7398_5A32A8(D_801FC624_5B8534, 0x10);

    *(volatile int *)0x80000000 = 1;
}
