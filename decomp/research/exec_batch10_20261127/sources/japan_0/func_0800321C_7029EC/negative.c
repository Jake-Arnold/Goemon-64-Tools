#include "m2c_types.h"
M2C_UNK func_080028B4_702084(void *);
extern u8 func_80034E8C_35A8C[];
extern M2C_UNK func_0800329C_702A6C;

void func_0800321C_7029EC(void *arg0, void *arg1) {
    if (M2C_FIELD(arg0, u16 *, 0xEE) & 1) {
        M2C_FIELD(arg1, f32 *, 0xC) += (1 - (M2C_FIELD(arg0, u16 *, 0xEE) & 2));
    }
    if (--M2C_FIELD(arg0, u16 *, 0xEE) == 0) {
        ((void (*)(M2C_UNK *))func_80034E8C_35A8C)(&func_0800329C_702A6C);
        func_080028B4_702084(arg0);
    }

    *(volatile s32 *)0x80000000 = 1;
}
