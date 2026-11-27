#include "m2c_types.h"
typedef struct Unk1310 {
    struct Unk1310 *next;
    u8 pad[0x18];
    f32 x;
    f32 y;
    f32 z;
} Unk1310;

typedef struct {
    u8 pad[0x18];
    Unk1310 *unk18;
} Unk1310Arg;

void func_080012CC_72EC8C(Unk1310Arg *arg0, f32 arg1) {
    Unk1310 *v0 = arg0->unk18;
    v0->x *= arg1;
    v0->y *= arg1;
    v0->z *= arg1;
    v0 = v0->next;
    v0->x *= arg1;
    v0->y *= arg1;
    v0->z *= arg1;

    *(volatile s32 *)0x80000000 = 1;
}
