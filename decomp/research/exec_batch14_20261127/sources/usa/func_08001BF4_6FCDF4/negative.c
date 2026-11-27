#include "m2c_types.h"

extern u8 func_80216E1C_5D22EC[];
extern u8 func_8003521C_35E1C[];
extern f32 D_080037C4_6FE9C4;
extern u8 func_08001C70_6FCE70[];

void func_08001BF4_6FCDF4(void *arg0, void *arg1) {
    f32 val;

    *(u32 *)((u8 *)arg0 + 0x60) = 0x80000221;
    *(u8 *)((u8 *)arg0 + 0x6C) = 0;
    ((void (*)(void *, u8))func_80216E1C_5D22EC)(arg0, *(u8 *)((u8 *)arg0 + 0xD0));
    val = D_080037C4_6FE9C4;
    *(f32 *)((u8 *)arg1 + 0x1C) = val;
    *(f32 *)((u8 *)arg1 + 0x20) = val;
    *(f32 *)((u8 *)arg1 + 0x24) = val;
    *(u16 *)((u8 *)arg0 + 0xE0) = *(u16 *)((u8 *)arg1 + 0x16);
    ((void (*)(void *))func_8003521C_35E1C)(func_08001C70_6FCE70);

    *(volatile int *)0x80000000 = 1;
}
