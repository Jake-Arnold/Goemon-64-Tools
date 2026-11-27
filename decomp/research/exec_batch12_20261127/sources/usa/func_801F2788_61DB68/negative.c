#include "m2c_types.h"

void func_8003521C_35E1C(void *);
f32 func_801D3018_5FE3F8(M2C_UNK, f32);
void func_801D5C30_601010(void *, s32, f32, u16, s32);
s32 func_801D5D98_601178(void *, s32, f32, f32);
void func_801D655C_60193C(void *, f32, f32, f32, f32);
void func_801F7AD0_622EB0(void *);
extern void func_801F2854_61DC34(void);

void func_801F2788_61DB68(void *arg0, M2C_UNK arg1) {
    if (func_801D3018_5FE3F8(arg1, 40.0f) == 0.0f) {
        func_801F7AD0_622EB0(arg0);
    }
    func_801D655C_60193C(arg0, -300.0f, 300.0f, 0.1f, 4.0f);
    M2C_FIELD(arg0, f32 *, 0x74) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    func_801D5C30_601010(arg0, M2C_FIELD(arg0, s32 *, 0x70), M2C_FIELD(arg0, f32 *, 0x78), func_801D5D98_601178(arg0, 0x30, 4.0f, 3.0f), 0);
    if (--M2C_FIELD(arg0, s32 *, 0x7C) == 0) {
        func_8003521C_35E1C(func_801F2854_61DC34);
    }

    *(volatile int *)0x80000000 = 1;
}
