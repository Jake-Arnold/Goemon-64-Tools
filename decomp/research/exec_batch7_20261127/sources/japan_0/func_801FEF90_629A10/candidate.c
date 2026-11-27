#include "m2c_types.h"
typedef struct {
    u8 pad0[0x8];
    f32 unk8;
} UnkSubSub_F9860;

typedef struct {
    u8 pad0[0x18];
    UnkSubSub_F9860 *unk18;
} UnkSub_F9860;

typedef struct {
    u8 pad0[0xC];
    f32 unkC;
} UnkA0_F9860;

typedef struct {
    u8 pad0[0xA0];
    UnkA0_F9860 unkA0;
    u8 padB0[0x1D8 - 0xB0];
    UnkSub_F9860 *unk1D8;
    u8 pad1DC[0x2C1 - 0x1DC];
    s8 unk2C1;
} UnkGlobal_F9860;

typedef struct {
    u8 pad0[0x7C];
    s32 unk7C;
} UnkArg0_F9860;

M2C_UNK func_80034E8C_35A8C(void (*)(void));
extern UnkGlobal_F9860 *D_80214600_63F080;
void func_801FF014_629A94(void);

void func_801FEF90_629A10(UnkArg0_F9860 *arg0, M2C_UNK arg1) {
    UnkA0_F9860 *temp_v1;
    UnkSubSub_F9860 *temp_a1;

    temp_v1 = &D_80214600_63F080->unkA0;
    temp_a1 = D_80214600_63F080->unk1D8->unk18;
    temp_v1->unkC = temp_a1->unk8;
    if (temp_v1->unkC <= -300.0f) {
        temp_v1->unkC = -300.0f;
        if (--arg0->unk7C == 0) {
            D_80214600_63F080->unk2C1 = 2;
            func_80034E8C_35A8C(func_801FF014_629A94);
        }
    }
}
