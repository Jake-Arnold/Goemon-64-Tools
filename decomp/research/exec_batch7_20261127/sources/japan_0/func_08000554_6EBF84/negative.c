#include "m2c_types.h"

void func_80034E8C_35A8C(void *);
extern M2C_UNK func_080005AC_6EBFDC;

typedef struct {
    u8 unk0[0x60];
    s32 unk60;
    u8 unk64[0x18];
    f32 unk7C;
    u8 unk80[0xD];
    s8 unk8D;
    u8 unk8E[0x42];
    f32 unkD0;
} UnkArg0;

typedef struct {
    u8 unk0[0xC];
    f32 unkC;
} UnkArg1;

void func_08000554_6EBF84(UnkArg0 *arg0, UnkArg1 *arg1) {
    void (*fn)(void *) = func_80034E8C_35A8C;

    arg0->unk60 |= 0x800000;
    arg0->unkD0 = arg1->unkC;
    arg0->unk7C = 3.0f;
    arg0->unk8D = 0x10;
    fn(&func_080005AC_6EBFDC);

    *(volatile s32 *)0x80000000 = 1;
}
