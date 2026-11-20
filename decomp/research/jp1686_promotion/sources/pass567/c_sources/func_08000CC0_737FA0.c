#include "../m2c_types.h"
extern void *D_8020151C_5BD4EC;

void func_08000CC0_737FA0(s32 arg0, f32 arg1, f32 arg2, f32 arg3) {
    M2C_FIELD(D_8020151C_5BD4EC, f32 *, 8) = arg1;
    M2C_FIELD(D_8020151C_5BD4EC, f32 *, 0xC) = arg2;
    M2C_FIELD(D_8020151C_5BD4EC, f32 *, 0x10) = arg3;
}
