#include "m2c_types.h"

typedef struct {
    u8 pad0[0x34];
    s32 unk34;
    u8 pad38[0x60];
    s32 unk98;
    s32 unk9C;
} Arg0_DABF4;

typedef struct {
    u8 pad0[0x16];
    s16 unk16;
} Arg1_DABF4;

void func_80034E8C_35A8C(void (*)(void));
void func_801D8DDC_60385C(Arg0_DABF4 *);
void func_801DE750_6091D0(Arg0_DABF4 *, Arg1_DABF4 *);
void func_801E0630_60B0B0(Arg0_DABF4 *, s32);
void func_801E0398_60AE18(void);

void func_801E0314_60AD94(Arg0_DABF4 *arg0, Arg1_DABF4 *arg1) {
    func_801DE750_6091D0(arg0, arg1);
    arg0->unk98 -= 0x13;
    if (arg0->unk98 < -0x31) {
        arg0->unk98 = -0x32;
        func_80034E8C_35A8C(func_801E0398_60AE18);
    }
    arg1->unk16 = arg0->unk98 + arg0->unk9C;
    if (arg0->unk34 != 0) {
        func_801E0630_60B0B0(arg0, arg0->unk34);
    }
    func_801D8DDC_60385C(arg0);
}
