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

M2C_UNK func_8003521C_35E1C(M2C_UNK *);
M2C_UNK func_801D614C_60152C(UnkArg0_DAE28 *, UnkArg1_DAE28 *);
M2C_UNK func_801D9030_604410(UnkArg0_DAE28 *);
extern UnkGlobal_DAE28 *D_8020EED0_63A2B0;
extern M2C_UNK func_801D9D64_605144;

void func_801DAE28_606208(UnkArg0_DAE28 *arg0, UnkArg1_DAE28 *arg1) {
    UnkGlobal_DAE28 *sp24;

    sp24 = D_8020EED0_63A2B0;
    func_801D614C_60152C(arg0, arg1);
    if (arg0->unk7C-- < 0) {
        arg1->unk28 = 0.0f;
        func_801D9030_604410(arg0);
        sp24->unk4 -= arg0->unkC8;
        func_8003521C_35E1C(&func_801D9D64_605144);
    }
    arg0->unk98 -= 8;
    arg1->unk16 = arg0->unk98 + arg0->unk9C;
}
