#include "m2c_types.h"

s16 func_8000E9F4_F5F4(f32, f32, void *);
void func_8003521C_35E1C(void *);
f32 func_801D2F40_5FE320(void *, f32);
void func_801D31CC_5FE5AC(void *, void *);
void func_801FC3FC_6277DC(void *);
void func_8020003C_62B41C(void *, s32);
extern u8 D_8020B420_636800[];
extern void func_801FCD1C_6280FC(void);

void func_801FCC64_628044(void *arg0, void *arg1) {
    M2C_FIELD(arg1, s16 *, 0x16) = func_8000E9F4_F5F4(0.0f, 0.0f, arg1);
    if (func_801D2F40_5FE320(arg1, 20.0f) == 0.0f) {
        func_8020003C_62B41C(arg0, 0x1A);
        if (--M2C_FIELD(arg0, s32 *, 0x84) != 0) {
            M2C_FIELD(arg0, s32 *, 0x7C) = 0x40;
            M2C_FIELD(arg0, f32 *, 0x74) = -M2C_FIELD(arg0, f32 *, 0x74);
            func_801D31CC_5FE5AC(arg0, D_8020B420_636800);
            func_8003521C_35E1C(func_801FCD1C_6280FC);
            return;
        }
        func_801FC3FC_6277DC(arg0);
    }
}
