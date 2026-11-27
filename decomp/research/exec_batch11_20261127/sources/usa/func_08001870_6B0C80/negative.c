#include "m2c_types.h"
void func_8003521C_35E1C(M2C_UNK *);
s32 func_8021B988_5D6E58(void *, f32, f32, f32, f32);
extern M2C_UNK func_0800105C_6B046C;

void func_08001870_6B0C80(void *arg0, M2C_UNK arg1) {
    if (((s32 (*)(void *, f32, f32, f32, f32))func_8021B988_5D6E58)(arg0, 0.0f, -100.0f, 45.0f, 1.0f) == 0) {
        ((void (*)(M2C_UNK *))func_8003521C_35E1C)(&func_0800105C_6B046C);
    }

    *(volatile int *)0x80000000 = 1;
}
