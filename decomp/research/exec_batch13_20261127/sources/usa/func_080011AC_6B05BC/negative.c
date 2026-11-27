#include "m2c_types.h"

void func_08000F88_6B0398(s32, void *);
extern u8 func_8003521C_35E1C[];
extern u8 func_80219E08_5D52D8[];
extern u8 func_80221C0C_5DD0DC[];
extern void func_0800121C_6B062C(void);
extern void func_08001BEC_6B0FFC(void);

void func_080011AC_6B05BC(s32 arg0, M2C_UNK arg1) {
    func_08000F88_6B0398(arg0, func_08001BEC_6B0FFC);
    ((void (*)(s32, s32, f32, s32))func_80221C0C_5DD0DC)(arg0, 0, 0.25f, 1);
    ((void (*)(s32, f32))func_80219E08_5D52D8)(arg0, 1.25f);
    ((void (*)(void *))func_8003521C_35E1C)(func_0800121C_6B062C);

    *(volatile int *)0x80000000 = 1;
}
