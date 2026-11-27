#include "m2c_types.h"

extern u8 func_8021BB8C_5D711C[];
extern u8 func_80034E8C_35A8C[];
extern f32 D_080037C4_702F94;
extern u8 func_08001C70_701440[];

void func_08001BF4_7013C4(void *arg0, void *arg1) {
    f32 val;

    *(u32 *)((u8 *)arg0 + 0x60) = 0x80000221;
    *(u8 *)((u8 *)arg0 + 0x6C) = 0;
    ((void (*)(void *, u8))func_8021BB8C_5D711C)(arg0, *(u8 *)((u8 *)arg0 + 0xD0));
    val = D_080037C4_702F94;
    *(f32 *)((u8 *)arg1 + 0x1C) = val;
    *(f32 *)((u8 *)arg1 + 0x20) = val;
    *(f32 *)((u8 *)arg1 + 0x24) = val;
    *(u16 *)((u8 *)arg0 + 0xE0) = *(u16 *)((u8 *)arg1 + 0x16);
    ((void (*)(void *))func_80034E8C_35A8C)(func_08001C70_701440);
}
