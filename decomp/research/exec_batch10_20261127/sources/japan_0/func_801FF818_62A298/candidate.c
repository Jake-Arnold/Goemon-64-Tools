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

void func_80034E8C_35A8C(void (*)(void));
void func_801F3D88_61E808(UnkArg0 *);
void func_801FFCF8_62A778(s32);
extern UnkGlobal *D_80214600_63F080;
void func_801FF920_62A3A0(void);

void func_801FF818_62A298(UnkArg0 *arg0, M2C_UNK arg1) {
    UnkSub *sub = &D_80214600_63F080->unkA0;
    func_801F3D88_61E808(arg0);
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
        func_801FFCF8_62A778(D_80214600_63F080->unk1D8);
        func_80034E8C_35A8C(func_801FF920_62A3A0);
    }
}
