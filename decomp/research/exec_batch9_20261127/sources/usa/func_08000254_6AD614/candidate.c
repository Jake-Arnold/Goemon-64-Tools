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
M2C_UNK func_80026AAC_276AC(Vec3f *, s32);
extern UnkPtr *D_801FC60C_5B851C;

void func_08000254_6AD614(s32 arg0) {
    LocalStruct sp20;

    sp20.pos.x = D_801FC60C_5B851C->pos.x;
    sp20.pos.y = D_801FC60C_5B851C->pos.y;
    sp20.pos.z = D_801FC60C_5B851C->pos.z;
    ((void (*)(Vec3f *, s32))func_80026AAC_276AC)(&sp20.pos, arg0);
}
