#include "m2c_types.h"

void func_8021EBE0_5DA170(void *, s32, s32);
void func_802213C4_5DC954(void *);
void func_8022B5B0_5E6B40(void *, u16);

void func_08000000_71FF50(void *arg0) {
    void (*fn1)(void *, u16) = func_8022B5B0_5E6B40;
    void (*fn2)(void *) = func_802213C4_5DC954;
    void (*fn3)(void *, s32, s32) = func_8021EBE0_5DA170;

    M2C_FIELD(arg0, s32 *, 0x60) = 0x12800F21;
    M2C_FIELD(arg0, s32 *, 0x64) = 0x20;
    fn1(arg0, M2C_FIELD(arg0, u16 *, 0xD2));
    fn2(arg0);
    fn3(arg0, 5, 0);

    *(volatile s32 *)0x80000000 = 1;
}
