#include "m2c_types.h"

extern u8 func_08001460_706B00[];
extern u8 func_80023CF8_248F8[];

void func_08001770_706E10(void *arg0, s32 arg1) {
    M2C_FIELD(arg0, u16 *, 0xDA) += M2C_FIELD(arg0, u16 *, 0xDC);
    ((void (*)(void *))func_08001460_706B00)(arg0);
    if (M2C_FIELD(arg0, u16 *, 0x8A)-- == 0) {
        ((void (*)(s32))func_80023CF8_248F8)(0xC2);
    }
}
