#include "m2c_types.h"

extern u8 func_8003521C_35E1C[];
extern struct {
    u8 pad[0x186];
    u8 unk_186;
} D_8015CC30_15D830;
extern u8 func_08002128_6B53C8[];
extern u8 func_08002460_6B5700[];

void func_080023E0_6B5680(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        if (++D_8015CC30_15D830.unk_186 < 4) {
            ((void (*)(void *))func_8003521C_35E1C)(func_08002128_6B53C8);
            return;
        }
        M2C_FIELD(arg0, s16 *, 0x8A) = 0xA;
        ((void (*)(void *))func_8003521C_35E1C)(func_08002460_6B5700);
    }

    *(volatile int *)0x80000000 = 1;
}
