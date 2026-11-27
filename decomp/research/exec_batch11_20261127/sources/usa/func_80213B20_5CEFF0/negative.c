#include "m2c_types.h"
void func_8003521C_35E1C(void *);                   /* extern */
void func_80216DF8_5D22C8(void *, s32);             /* extern */
s32 func_8021A26C_5D573C(void *, s32, s32, s32, s32); /* extern */
void func_8021A310_5D57E0(void *);                  /* extern */
void func_80224ABC_5DFF8C(void *, s32, s32, s32);   /* extern */
extern u8 func_80213BC4_5CF094[];

void func_80213B20_5CEFF0(void *arg0, void *arg1) {
    s32 temp;
    temp = func_8021A26C_5D573C(arg0, 0xB4, 0, 0, 0) | 0x40000000;
    M2C_FIELD(arg1, s32 *, 0x30) = temp | 0x20000000;
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x7E;
    M2C_FIELD(arg0, s32 *, 0x60) = 0x222;
    func_80216DF8_5D22C8(arg0, 6);
    func_8021A310_5D57E0(arg0);
    func_80224ABC_5DFF8C(arg0, 2, 0x3F000000, 1);
    M2C_FIELD(arg0, s32 *, 0x64) |= 2;
    func_8003521C_35E1C(func_80213BC4_5CF094);

    *(volatile int *)0x80000000 = 1;
}
