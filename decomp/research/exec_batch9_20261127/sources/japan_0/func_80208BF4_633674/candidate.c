#include "m2c_types.h"

typedef struct {
    u8 pad0[0x7C];
    s32 unk7C;
    s32 unk80;
} Obj0_802034C4;

typedef struct {
    u8 pad0[0x8];
    f32 unk8;
    f32 unkC;
    f32 unk10;
} Obj1_802034C4;

void func_801E52CC_60FD4C(Obj0_802034C4 *, s32, f32, f32, f32, f32, f32, f32, f32, f32);
void func_801E57A8_610228(Obj0_802034C4 *, f32, s32, s32, f32, f32, f32, f32);
void func_802096B8_634138(void);

void func_80208BF4_633674(Obj0_802034C4 *arg0, Obj1_802034C4 *arg1) {
    func_802096B8_634138();
    if (--arg0->unk7C > 0) {
        if (!(arg0->unk7C & 7)) {
            func_801E52CC_60FD4C(arg0, 0, 1.0f, 0.1f, arg1->unk8, arg1->unkC + 20.0f, arg1->unk10 + 20.0f, 20.0f, 20.0f, 20.0f);
        }
    } else {
        arg0->unk7C = 0;
    }
    if (--arg0->unk80 == 0) {
        func_801E57A8_610228(arg0, 3.0f, 0, 3, 1.5f, arg1->unk8, arg1->unkC + 30.0f, arg1->unk10 + 40.0f);
        arg0->unk80 = 0x10;
    }
}
