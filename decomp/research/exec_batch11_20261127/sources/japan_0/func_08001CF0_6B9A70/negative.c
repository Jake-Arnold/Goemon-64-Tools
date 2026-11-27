#include "m2c_types.h"
void func_80034E8C_35A8C(M2C_UNK *);
void func_8021B3BC_5D694C(void *, s32, s32, s32);
extern M2C_UNK func_08001D4C_6B9ACC;

void func_08001CF0_6B9A70(void *arg0, M2C_UNK arg1) {
    ((void (*)(void *, s32, s32, s32))func_8021B3BC_5D694C)(arg0, 0, 0x3E2AAAAB, 1);
    M2C_FIELD(arg0, s16 *, 0x8A) = 0x1E;
    ((void (*)(M2C_UNK *))func_80034E8C_35A8C)(&func_08001D4C_6B9ACC);

    *(volatile int *)0x80000000 = 1;
}
