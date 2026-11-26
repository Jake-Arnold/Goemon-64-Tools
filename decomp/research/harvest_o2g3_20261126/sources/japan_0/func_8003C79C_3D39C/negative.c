#include "m2c_types.h"
extern void *D_80178E00_179A00;
extern s32 D_80178E04_179A04;

void func_8003C79C_3D39C(void) {
    M2C_FIELD(D_80178E00_179A00, s32 *, 0x6C) = (s32) D_80178E04_179A04;

    *(volatile s32 *)0x80000000 = 1;
}
