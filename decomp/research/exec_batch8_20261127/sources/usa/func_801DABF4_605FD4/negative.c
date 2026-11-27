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

void func_8003521C_35E1C(void (*)(void));
void func_801D36BC_5FEA9C(Arg0_DABF4 *);
void func_801D9030_604410(Arg0_DABF4 *, Arg1_DABF4 *);
void func_801DAF10_6062F0(Arg0_DABF4 *, s32);
void func_801DAC78_606058(void);

void func_801DABF4_605FD4(Arg0_DABF4 *arg0, Arg1_DABF4 *arg1) {
    func_801D9030_604410(arg0, arg1);
    arg0->unk98 -= 0x13;
    if (arg0->unk98 < -0x31) {
        arg0->unk98 = -0x32;
        func_8003521C_35E1C(func_801DAC78_606058);
    }
    arg1->unk16 = arg0->unk98 + arg0->unk9C;
    if (arg0->unk34 != 0) {
        func_801DAF10_6062F0(arg0, arg0->unk34);
    }
    func_801D36BC_5FEA9C(arg0);

    *(volatile s32 *)0x80000000 = 1;
}
