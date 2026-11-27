#include "m2c_types.h"
extern f32 D_08001858_734788;

void func_08000FC8_733EF8(void *arg0) {
    M2C_FIELD(arg0, f32 *, 0x80) = D_08001858_734788;
    M2C_FIELD(arg0, s32 *, 0x60) |= 0x02800300;
    M2C_FIELD(arg0, s8 *, 0x75) = 0xA;
    M2C_FIELD(arg0, s32 *, 0xD4) = 1;

    *(volatile s32 *)0x80000000 = 1;
}
