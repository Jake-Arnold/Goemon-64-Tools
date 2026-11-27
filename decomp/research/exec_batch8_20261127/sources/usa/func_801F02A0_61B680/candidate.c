#include "m2c_types.h"

void func_8003521C_35E1C(void (*)(void));
f32 func_801D2F40_5FE320(s32, f32);
void func_801D31CC_5FE5AC(s32, void *);
s32 func_801D3CE4_5FF0C4(f32, f32, f32, s32, s32);
void func_801D3F00_5FF2E0(s32, s32, s32);
void func_801F76D0_622AB0(s32, s32);
extern u8 D_8020B260_636640[];
void func_801F0330_61B710(void);

void func_801F02A0_61B680(s32 arg0, s32 arg1) {
    func_801F76D0_622AB0(arg0, arg1);
    func_801D3F00_5FF2E0(arg0, 0, 8);
    if ((func_801D3CE4_5FF0C4(0.0f, 0.0f, 0.0f, arg0, 0xA) != 0) &&
        (func_801D2F40_5FE320(arg1, 50.0f) == 0.0f)) {
        func_801D31CC_5FE5AC(arg0, D_8020B260_636640);
        func_8003521C_35E1C(func_801F0330_61B710);
    }
}
