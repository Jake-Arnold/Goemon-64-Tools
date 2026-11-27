#include "m2c_types.h"
typedef struct {
    u8 pad0[0x7C];
    s32 unk7C;
    u8 pad80[0x18];
    s32 unk98;
    s32 unk9C;
    u8 padA0[0x28];
    s32 unkC8;
} UnkArg0_DAE28;

typedef struct {
    u8 pad0[0x16];
    s16 unk16;
    u8 pad18[0x10];
    f32 unk28;
} UnkArg1_DAE28;

typedef struct {
    u8 pad0[0x4];
    f32 unk4;
} UnkGlobal_DAE28;

M2C_UNK func_80034E8C_35A8C(M2C_UNK *);
M2C_UNK func_801DB86C_6062EC(UnkArg0_DAE28 *, UnkArg1_DAE28 *);
M2C_UNK func_801DE750_6091D0(UnkArg0_DAE28 *);
extern UnkGlobal_DAE28 *D_80214600_63F080;
extern M2C_UNK func_801DF484_609F04;

void func_801E0548_60AFC8(UnkArg0_DAE28 *arg0, UnkArg1_DAE28 *arg1) {
    UnkGlobal_DAE28 *sp24;

    sp24 = D_80214600_63F080;
    func_801DB86C_6062EC(arg0, arg1);
    if (arg0->unk7C-- < 0) {
        arg1->unk28 = 0.0f;
        func_801DE750_6091D0(arg0);
        sp24->unk4 -= arg0->unkC8;
        func_80034E8C_35A8C(&func_801DF484_609F04);
    }
    arg0->unk98 -= 8;
    arg1->unk16 = arg0->unk98 + arg0->unk9C;
}
