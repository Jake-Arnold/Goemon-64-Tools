typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef short s16;typedef unsigned int u32;typedef int s32;typedef float f32;typedef double f64;typedef unsigned long long u64;typedef long long s64;
#include "m2c_macros.h"
s32 func_8000FFF0_10BF0(M2C_UNK, M2C_UNK, M2C_UNK, M2C_UNK, M2C_UNK *, s32); /* extern */
M2C_UNK func_80013654_14254(M2C_UNK *);             /* extern */
extern M2C_UNK D_08000D10_6B1DE0;
extern M2C_UNK D_801D89C0_66AF10;
extern s32 D_801E7C0C_67A15C;
extern s32 D_801E7C10_67A160;
extern u8 func_08001D00_6B5C00;

void func_801D0B90_6630E0(void) {
    func_80013654_14254(&D_801D89C0_66AF10);
    D_801E7C0C_67A15C = func_8000FFF0_10BF0(0x20, 0x40, 0x10, 0, &D_08000D10_6B1DE0, 0x4CD);
    D_801E7C10_67A160 = func_8000FFF0_10BF0(0x40, 0x20, 0x10, 0, (M2C_UNK*)(&func_08001D00_6B5C00 + 0x10), 0x4CD);
}
