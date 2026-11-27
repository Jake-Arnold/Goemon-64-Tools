#include "m2c_types.h"

extern u8 func_80034E8C_35A8C[];
extern u8 func_8021E548_5D9AD8[];
extern u8 func_08003044_6E17D4[];

void func_08002FD8_6E1768(void *arg0, void *arg1) {
    u8 *temp_v0;

    if (((s32 (*)(void *, s32))func_8021E548_5D9AD8)(arg0, 0x10) == 0) {
        *(s8 *)((u8 *)arg1 + 0x7C) = 1;
        temp_v0 = *(u8 **)((u8 *)arg0 + 0x84);
        *(f32 *)((u8 *)arg0 + 0xDC) = *(f32 *)(temp_v0 + 8);
        *(f32 *)((u8 *)arg0 + 0xE0) = *(f32 *)(temp_v0 + 0x10);
        ((void (*)(void *))func_80034E8C_35A8C)(func_08003044_6E17D4);
    }
}
