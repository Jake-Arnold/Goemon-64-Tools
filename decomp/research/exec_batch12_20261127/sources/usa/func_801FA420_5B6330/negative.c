#include "m2c_types.h"

typedef struct {
    u8 pad0[0xAE29];
    u8 unkAE29;
    u8 padAE2A[2];
    s32 unkAE2C;
    u16 unkAE30;
} Struct_800BCCC0;

void func_801FA4FC_5B640C(u16, s16, s16, s16, u16, s32);
extern Struct_800BCCC0 D_800BCCC0_BD8C0;

void func_801FA420_5B6330(u16 arg0, s16 arg1, s16 arg2, s16 arg3, u16 arg4, s32 arg5, u16 arg6) {
    func_801FA4FC_5B640C(arg0, arg1, arg2, arg3, arg4, 0);
    D_800BCCC0_BD8C0.unkAE2C = arg5;
    D_800BCCC0_BD8C0.unkAE30 = arg6;
    D_800BCCC0_BD8C0.unkAE29 |= 8;

    *(volatile int *)0x80000000 = 1;
}
