#include "m2c_types.h"
typedef struct {
    u8 pad0[0x7C];
    s32 unk7C;
    u8 pad80[0x10];
    f32 unk90;
    f32 unk94;
} UnkArg0;

typedef struct {
    u8 pad0[0x8];
    f32 unk8;
    f32 unkC;
} UnkSub;

typedef struct {
    u8 pad0[0xA0];
    UnkSub unkA0;
    u8 padB0[0x128];
    s32 unk1D8;
} UnkGlobal;

void func_8003521C_35E1C(void (*)(void));
void func_801EE658_619A38(UnkArg0 *);
void func_801FA5C8_6259A8(s32);
extern UnkGlobal *D_8020EED0_63A2B0;
void func_801FA1F0_6255D0(void);

void func_801FA0E8_6254C8(UnkArg0 *arg0, M2C_UNK arg1) {
    UnkSub *sub = &D_8020EED0_63A2B0->unkA0;
    func_801EE658_619A38(arg0);
    if (--arg0->unk7C <= 0) {
        arg0->unk90 += 0.875;
        if (arg0->unk90 >= -300.0f) {
            arg0->unk90 = -300.0f;
        }
        sub->unk8 = arg0->unk90;
        arg0->unk94 += 0.625;
        if (arg0->unk94 >= 50.0f) {
            arg0->unk94 = 50.0f;
        }
        sub->unkC = arg0->unk94;
    }
    if (arg0->unk7C == -0x55) {
        func_801FA5C8_6259A8(D_8020EED0_63A2B0->unk1D8);
        func_8003521C_35E1C(func_801FA1F0_6255D0);
    }

    *(volatile s32 *)0x80000000 = 1;
}
