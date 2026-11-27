#include "m2c_types.h"
extern void func_8003521C_35E1C(void *);
extern M2C_UNK func_08002144_6B1554;

void func_080020F4_6B1504(void *arg0, M2C_UNK arg1) {
    void (*fn)(void *) = func_8003521C_35E1C;
    if (M2C_FIELD(arg0, s32 *, 0xE0)++ < 10) {
        M2C_FIELD(arg0, s32 *, 0xE0)++;
    } else {
        fn(&func_08002144_6B1554);
    }

    *(volatile s32 *)0x80000000 = 1;
}
