#include "m2c_types.h"

typedef struct {
    u8 pad0[0x7C];
    s32 unk7C;
    s32 unk80;
} Arg0_20269C;

typedef struct {
    u8 pad0[0x8];
    f32 x;
    f32 y;
    f32 z;
} Arg1_20269C;

void func_801E52CC_60FD4C(Arg0_20269C *, s32, f32, f32, f32, f32, f32, f32, f32, f32);
void func_801E57A8_610228(Arg0_20269C *, f32, s32, s32, f32, f32, f32, f32);
void func_802096B8_634138(Arg0_20269C *, Arg1_20269C *);

void func_80207DCC_63284C(Arg0_20269C *arg0, Arg1_20269C *arg1) {
    func_802096B8_634138(arg0, arg1);
    if (--arg0->unk7C > 0) {
        if ((arg0->unk7C & 7) == 0) {
            func_801E52CC_60FD4C(
                arg0, 0, 2.0f, 0.1f,
                arg1->x, arg1->y + 40.0f, arg1->z + 50.0f,
                30.0f, 30.0f, 20.0f
            );
        }
    } else {
        arg0->unk7C = 0;
    }
    if (--arg0->unk80 == 0) {
        func_801E57A8_610228(
            arg0, 2.0f, 0, 4, 2.0f,
            arg1->x, arg1->y + 40.0f, arg1->z + 60.0f
        );
        arg0->unk80 = 0x10;
    }
}
