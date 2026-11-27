#include "m2c_types.h"
void func_80033898_34498(u16, u16, u16, f32 *, f32 *, f32 *); /* extern */
extern f32 D_8020B5AC_5C74BC;

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

void func_801E6F4C_5A2E5C(Arg0 *arg0) {
    Unk18 *unk18 = arg0->unk18;
    f32 x = 0.0f;
    f32 y = 0.0f;
    f32 z = D_8020B5AC_5C74BC;

    func_80033898_34498(unk18->rx, unk18->ry, unk18->rz, &x, &y, &z);
    unk18->x += x;
    unk18->y += y;
    unk18->z += z;

    *(volatile int *)0x80000000 = 1;
}
