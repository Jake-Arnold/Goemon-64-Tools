#include "m2c_types.h"

extern u8 func_800240DC_24CDC[];
extern u8 func_8003521C_35E1C[];
extern M2C_UNK func_080065F0_6B9890;

void func_0800658C_6B982C(s32 arg0, void *arg1) {
    if (((s32 (*)(s32))func_800240DC_24CDC)(0x133) != 0) {
        if (++M2C_FIELD(arg1, u16 *, 0x16) == 0x29) {
            ((void (*)(M2C_UNK *))func_8003521C_35E1C)(&func_080065F0_6B9890);
        }
    }

    *(volatile int *)0x80000000 = 1;
}
