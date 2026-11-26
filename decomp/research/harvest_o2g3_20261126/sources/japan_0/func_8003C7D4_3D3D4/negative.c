#include "m2c_types.h"
extern void *D_80178E00_179A00;
extern s32 D_80178E04_179A04;

void func_8003C7D4_3D3D4(void) {
    M2C_FIELD(D_80178E00_179A00, s8 *, 0x70) = 0;
    M2C_FIELD(D_80178E00_179A00, s32 *, 0x74) = (s32) D_80178E04_179A04;

    *(volatile s32 *)0x80000000 = 1;
}
