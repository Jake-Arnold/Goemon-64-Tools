#include "m2c_types.h"
void func_8003521C_35E1C(M2C_UNK *);
extern void *D_801FC604_5B8514;
extern M2C_UNK func_08005564_6CD774;

void func_080054EC_6CD6FC(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, u16 *, 0x8A)++ >= 0x5A) {
        M2C_FIELD(D_801FC604_5B8514, u16 *, 0x94) = (M2C_FIELD(D_801FC604_5B8514, u16 *, 0x94) - 0x10) & 0x3FF;
        if (M2C_FIELD(M2C_FIELD(arg0, void **, 0x84), u16 *, 0x16) == 0x380) {
            M2C_FIELD(arg0, u16 *, 0x8A) = 0;
            ((void (*)(M2C_UNK *))func_8003521C_35E1C)(&func_08005564_6CD774);
        }
    }

    *(volatile int *)0x80000000 = 1;
}
