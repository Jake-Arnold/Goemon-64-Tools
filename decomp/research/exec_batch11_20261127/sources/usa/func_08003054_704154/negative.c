#include "m2c_types.h"
M2C_UNK func_080029CC_703ACC(void *);               /* extern */
extern u8 func_8003521C_35E1C[];
extern M2C_UNK func_080030B0_7041B0;

void func_08003054_704154(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, u16 *, 0x8A)-- == 0) {
        ((M2C_UNK (*)(M2C_UNK *, void *))func_8003521C_35E1C)(&func_080030B0_7041B0, arg0);
    }
    func_080029CC_703ACC(arg0);

    *(volatile int *)0x80000000 = 1;
}
