#include "m2c_types.h"
extern u8 func_8003521C_35E1C[];
extern u8 func_80221B48_5DD018[];
extern u8 D_3B07A[];
extern s32 D_8015C5C8_15D1C8;
extern M2C_UNK func_08000150_71BBD0;

void func_080000E8_71BB68(void *arg0, M2C_UNK arg1) {
    if (M2C_FIELD(arg0, s32 *, 0xD8) != 1 || *(u16 *)(D_3B07A + D_8015C5C8_15D1C8) == 0xC00F) {
        ((M2C_UNK (*)(void))func_80221B48_5DD018)();
        ((M2C_UNK (*)(M2C_UNK *))func_8003521C_35E1C)(&func_08000150_71BBD0);
    }

    *(volatile int *)0x80000000 = 1;
}
