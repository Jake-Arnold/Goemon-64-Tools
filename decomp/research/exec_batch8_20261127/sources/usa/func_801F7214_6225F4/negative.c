#include "m2c_types.h"

typedef struct {
    f32 x;
    f32 y;
    f32 z;
} Vec3f_F7214;

typedef struct {
    u8 pad0[0x8];
    Vec3f_F7214 pos;
} Unk18_F7214;

typedef struct {
    u8 pad0[0x18];
    Unk18_F7214 *unk18;
} Arg0_F7214;

typedef struct {
    u8 pad0[0x178];
    Vec3f_F7214 vec;
} Global_F7214;

extern Global_F7214 *D_8020EED0_63A2B0;

void func_801F7214_6225F4(Arg0_F7214 *arg0) {
    Vec3f_F7214 *v0 = &D_8020EED0_63A2B0->vec;
    Unk18_F7214 *v1 = arg0->unk18;

    v1->pos.x += v0->x;
    v1->pos.y += v0->y;
    v1->pos.z += v0->z;

    *(volatile s32 *)0x80000000 = 1;
}
