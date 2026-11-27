#include "m2c_types.h"

extern u8 func_80023D9C_2499C[];
extern u8 func_80034E8C_35A8C[];
extern M2C_UNK func_0800658C_6BE30C;

void func_08006528_6BE2A8(s32 arg0, void *arg1) {
    if (((s32 (*)(s32))func_80023D9C_2499C)(0x133) != 0) {
        if (++M2C_FIELD(arg1, u16 *, 0x16) == 0x29) {
            ((void (*)(M2C_UNK *))func_80034E8C_35A8C)(&func_0800658C_6BE30C);
        }
    }

    *(volatile int *)0x80000000 = 1;
}
