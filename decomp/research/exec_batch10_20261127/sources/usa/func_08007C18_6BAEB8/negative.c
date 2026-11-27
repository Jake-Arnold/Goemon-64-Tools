#include "m2c_types.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);
extern M2C_UNK func_08007C70_6BAF10;

void func_08007C18_6BAEB8(void *arg0, M2C_UNK arg1) {
    u16 val = --M2C_FIELD(arg0, u16 *, 0x8A);

    if (val < 0x1F) {
        M2C_FIELD(arg0, s32 *, 0xE8) |= 0x80;
        if (val == 0) {
            M2C_UNK (*fn)(M2C_UNK *) = func_8003521C_35E1C;
            fn(&func_08007C70_6BAF10);
        }
    }

    *(volatile s32 *)0x80000000 = 1;
}
