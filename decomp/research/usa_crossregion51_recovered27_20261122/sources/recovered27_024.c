typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef short s16;typedef unsigned int u32;typedef int s32;typedef float f32;typedef double f64;typedef unsigned long long u64;typedef long long s64;
#include "m2c_macros.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D3018_5FE3F8(M2C_UNK, M2C_UNK);     /* extern */
M2C_UNK func_801D5C30_601010(void *, s32, s32, s32, s32); /* extern */
s32 func_801D5D98_601178(void *, M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_801D614C_60152C(void *);               /* extern */
M2C_UNK func_801FF944_62AD24();                     /* static */
extern void *D_8020EF40_63A320;

void func_801FF8B4_62AC94(void *arg0, M2C_UNK arg1) {
    s32 temp_t9;

    func_801D3018_5FE3F8(arg1, 0x42700000);
    M2C_FIELD(D_8020EF40_63A320, s8 *, 0x816) = 2;
    func_801D614C_60152C(arg0);
    temp_t9 = --M2C_FIELD(arg0, s32 *, 0x7C);
    if (temp_t9 <= 0) {
        func_8003521C_35E1C(func_801FF944_62AD24);
    }
    func_801D5C30_601010(arg0, M2C_FIELD(arg0, s32 *, 0x70), M2C_FIELD(arg0, s32 *, 0x78), func_801D5D98_601178(arg0, 0x30, 0x41200000, 0x41000000) & 0xFFFF, 0);
}
