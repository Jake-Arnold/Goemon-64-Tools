#include "m2c_types.h"

s32 func_080016A8_6D0788(void *);
extern u8 func_8021E71C_5D9BEC[];
extern u8 func_8021ADD0_5D62A0[];
extern u8 func_8021927C_5D474C[];
extern u8 func_8021B09C_5D656C[];

void func_08001B40_6D0C20(void *arg0, void *arg1) {
    if (func_080016A8_6D0788(arg0) == 0) {
        ((void (*)(void *, s32))func_8021E71C_5D9BEC)(arg0, 0x3F800000);
        *(s16 *)((u8 *)arg1 + 0x16) = ((s16 (*)(f32, f32))func_8021ADD0_5D62A0)(
            *(f32 *)((u8 *)arg0 + 0x78),
            *(f32 *)((u8 *)arg0 + 0x80)
        );
        ((void (*)(void *))func_8021927C_5D474C)(arg0);
        ((void (*)(void *, s32, s32))func_8021B09C_5D656C)(arg0, 0, 0);
    }
}
