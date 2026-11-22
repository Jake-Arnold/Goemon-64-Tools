typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef short s16;typedef unsigned int u32;typedef int s32;typedef float f32;typedef double f64;typedef unsigned long long u64;typedef long long s64;
#include "m2c_macros.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D5C30_601010(void *, s32, s32, s32, s32); /* extern */
s32 func_801D5D98_601178(void *, M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_801D60E4_6014C4();                     /* extern */
M2C_UNK func_801E5F64_611344();                     /* static */
M2C_UNK func_801EEE54_61A234(void *);               /* static */
M2C_UNK func_801EEEA0_61A280(void *);               /* static */

void func_801E5EE0_6112C0(void *arg0, M2C_UNK arg1) {
    s32 temp_t7;

    func_801D60E4_6014C4();
    func_801EEE54_61A234(arg0);
    func_801EEEA0_61A280(arg0);
    temp_t7 = --M2C_FIELD(arg0, s32 *, 0x7C);
    if (temp_t7 <= 0) {
        func_8003521C_35E1C(func_801E5F64_611344);
    }
    func_801D5C30_601010(arg0, M2C_FIELD(arg0, s32 *, 0x70), M2C_FIELD(arg0, s32 *, 0x78), func_801D5D98_601178(arg0, 0x30, 0x41200000, 0x41000000) & 0xFFFF, 0);
}
