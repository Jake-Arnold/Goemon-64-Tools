#include "m2c_types.h"

void func_8000364C_424C(s32);
void func_80006124_6D24(u16, s32);
extern u8 D_3AFE0[];
extern s32 g_system_ptr;

void func_800060D0_6CD0(u8 arg0, u16 arg1, s32 arg2) {
    func_80006124_6D24(arg1, arg2);
    *(s16 *)(D_3AFE0 + g_system_ptr) = arg0 + 0x220;
    func_8000364C_424C(0xC);
}
