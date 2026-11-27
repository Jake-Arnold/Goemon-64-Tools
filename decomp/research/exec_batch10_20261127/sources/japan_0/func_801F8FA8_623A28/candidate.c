#include "m2c_types.h"

typedef struct {
    u8 pad0[0x74];
    f32 unk74;
    u8 pad78[0x8];
    s32 unk80;
} UnkArg0;

void func_80034E8C_35A8C(void (*)(void));
void func_801D88EC_60336C(UnkArg0 *, void *);
s32 func_801DBA50_6064D0(UnkArg0 *, u32);
void func_801FCE00_627880(UnkArg0 *);
extern u8 D_802109D0_63B450[];
void func_801F900C_623A8C(void);

void func_801F8FA8_623A28(UnkArg0 *arg0, M2C_UNK arg1) {
    arg0->unk74 = 8.0f;
    func_801FCE00_627880(arg0);
    if (func_801DBA50_6064D0(arg0, 0xC2F00000U) != 0) {
        arg0->unk80 = 0xC8;
        func_801D88EC_60336C(arg0, D_802109D0_63B450);
        func_80034E8C_35A8C(func_801F900C_623A8C);
    }
}
