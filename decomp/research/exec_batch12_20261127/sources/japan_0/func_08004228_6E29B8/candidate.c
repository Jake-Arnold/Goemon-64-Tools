#include "m2c_types.h"

extern u8 func_80034E8C_35A8C[];
extern u8 func_8021B3BC_5D694C[];
extern u8 func_80222718_5DDCA8[];
extern u8 func_08003F48_6E26D8[];

void func_08004228_6E29B8(void *arg0, s32 arg1) {
    if (((s32 (*)(void *, u16, s32))func_80222718_5DDCA8)(arg0, *(u16 *)((u8 *)arg0 + 0xDC), 0x20) != 0) {
        ((void (*)(void *, s32, f32, s32))func_8021B3BC_5D694C)(arg0, 0, 0.5f, 4);
        ((void (*)(void *))func_80034E8C_35A8C)(func_08003F48_6E26D8);
    }
}
