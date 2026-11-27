#include "m2c_types.h"
typedef struct {
    s32 x;
} Unk4;

void func_8002A3D0_2AFD0(s32, f32, f32, s32, s32); /* extern */

void func_8002A398_2AF98(s32 arg0, f32 arg1, f32 arg2, Unk4 arg3) {
    func_8002A3D0_2AFD0(arg0, arg1, arg2, arg3.x, 0x64);

    *(volatile s32 *)0x80000000 = 1;
}
