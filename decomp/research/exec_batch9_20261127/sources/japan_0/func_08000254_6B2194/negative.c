#include "m2c_types.h"
typedef struct {
    f32 x;
    f32 y;
    f32 z;
} Vec3f;
typedef struct {
    u8 pad0[0x8];
    Vec3f pos;
} UnkPtr;
typedef struct {
    Vec3f pos;
    u8 padC[0x44];
} LocalStruct;
M2C_UNK func_8002676C_2736C(Vec3f *, s32);
extern UnkPtr *D_8020151C_5BD4EC;

void func_08000254_6B2194(s32 arg0) {
    LocalStruct sp20;

    sp20.pos.x = D_8020151C_5BD4EC->pos.x;
    sp20.pos.y = D_8020151C_5BD4EC->pos.y;
    sp20.pos.z = D_8020151C_5BD4EC->pos.z;
    ((void (*)(Vec3f *, s32))func_8002676C_2736C)(&sp20.pos, arg0);

    *(volatile s32 *)0x80000000 = 1;
}
