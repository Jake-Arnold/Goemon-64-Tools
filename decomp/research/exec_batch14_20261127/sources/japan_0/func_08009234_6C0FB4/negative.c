#include "m2c_types.h"

extern u8 func_80023D9C_2499C[];
extern u8 func_80034E8C_35A8C[];
extern s32 g_system_ptr;
extern u8 D_CF8E8[];
extern u8 func_080092A8_6C1028[];

void func_08009234_6C0FB4(void *arg0, M2C_UNK arg1) {
    if (((s32 (*)(s32))func_80023D9C_2499C)(0x12E) != 0) {
        M2C_FIELD(arg0, s8 *, 0xDD) = 0x38;
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x5A;
        M2C_FIELD(*(void **)(D_CF8E8 + g_system_ptr), s16 *, 0x22) = 0;
        ((void (*)(void *))func_80034E8C_35A8C)(func_080092A8_6C1028);
    }

    *(volatile int *)0x80000000 = 1;
}
