#include "m2c_types.h"

void func_80219E70_5D5340(void *, s32, s32);
void func_8021C654_5D7B24(void *);
void func_80226840_5E1D10(void *, u16);

void func_08000000_71BA80(void *arg0) {
    void (*fn1)(void *, u16) = func_80226840_5E1D10;
    void (*fn2)(void *) = func_8021C654_5D7B24;
    void (*fn3)(void *, s32, s32) = func_80219E70_5D5340;

    M2C_FIELD(arg0, s32 *, 0x60) = 0x12800F21;
    M2C_FIELD(arg0, s32 *, 0x64) = 0x20;
    fn1(arg0, M2C_FIELD(arg0, u16 *, 0xD2));
    fn2(arg0);
    fn3(arg0, 5, 0);

    *(volatile s32 *)0x80000000 = 1;
}
