#include "m2c_types.h"
M2C_UNK func_080028B4_6FDAB4(void *);
extern u8 func_8003521C_35E1C[];
extern M2C_UNK func_0800329C_6FE49C;

void func_0800321C_6FE41C(void *arg0, void *arg1) {
    if (M2C_FIELD(arg0, u16 *, 0xEE) & 1) {
        M2C_FIELD(arg1, f32 *, 0xC) += (1 - (M2C_FIELD(arg0, u16 *, 0xEE) & 2));
    }
    if (--M2C_FIELD(arg0, u16 *, 0xEE) == 0) {
        ((void (*)(M2C_UNK *))func_8003521C_35E1C)(&func_0800329C_6FE49C);
        func_080028B4_6FDAB4(arg0);
    }
}
