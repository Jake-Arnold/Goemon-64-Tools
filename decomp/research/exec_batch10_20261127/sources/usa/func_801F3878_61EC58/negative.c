#include "m2c_types.h"

typedef struct {
    u8 pad0[0x74];
    f32 unk74;
    u8 pad78[0x8];
    s32 unk80;
} UnkArg0;

void func_8003521C_35E1C(void (*)(void));
void func_801D31CC_5FE5AC(UnkArg0 *, void *);
s32 func_801D6330_601710(UnkArg0 *, u32);
void func_801F76D0_622AB0(UnkArg0 *);
extern u8 D_8020B2A0_636680[];
void func_801F38DC_61ECBC(void);

void func_801F3878_61EC58(UnkArg0 *arg0, M2C_UNK arg1) {
    arg0->unk74 = 8.0f;
    func_801F76D0_622AB0(arg0);
    if (func_801D6330_601710(arg0, 0xC2F00000U) != 0) {
        arg0->unk80 = 0xC8;
        func_801D31CC_5FE5AC(arg0, D_8020B2A0_636680);
        func_8003521C_35E1C(func_801F38DC_61ECBC);
    }

    *(volatile s32 *)0x80000000 = 1;
}
