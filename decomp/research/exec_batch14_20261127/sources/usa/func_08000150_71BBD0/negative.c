#include "m2c_types.h"

extern u8 func_8021A4E4_5D59B4[];
extern u8 func_80220F70_5DC440[];
extern u8 func_802268A8_5E1D78[];

void func_08000150_71BBD0(void *arg0, void *arg1) {
    if (*(s32 *)((u8 *)arg0 + 0xD8) != 0) {
        if (++*(s32 *)((u8 *)arg0 + 0xD8) == 3) {
            ((void (*)(void *, s32))func_8021A4E4_5D59B4)(arg0, 0x40000000);
            *(s32 *)((u8 *)arg0 + 0xD8) = 0;
        }
    }
    if (((s32 (*)(void *))func_80220F70_5DC440)(arg0) == 0) {
        ((void (*)(void *))func_802268A8_5E1D78)(arg0);
    }

    *(volatile int *)0x80000000 = 1;
}
