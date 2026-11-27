#include "m2c_types.h"

extern u8 func_8003521C_35E1C[];
extern u8 func_8021A26C_5D573C[];
extern u8 func_08004DDC_6C452C[];

void func_08004D64_6C44B4(void *arg0, s32 arg1) {
    *(u8 *)((u8 *)arg0 + 0xDC) -= 8;
    ((void (*)(void *, u8, s32, s32, s32))func_8021A26C_5D573C)(arg0, *(u8 *)((u8 *)arg0 + 0xDC), 0xC8, 0, 0);
    if (*(u8 *)((u8 *)arg0 + 0xDC) < 9) {
        *(u8 *)((u8 *)arg0 + 0xDC) = 8;
        ((void (*)(void *))func_8003521C_35E1C)(func_08004DDC_6C452C);
    }
}
