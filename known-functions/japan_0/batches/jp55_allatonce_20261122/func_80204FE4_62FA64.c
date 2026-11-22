typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef short s16;typedef unsigned int u32;typedef int s32;typedef float f32;typedef double f64;typedef unsigned long long u64;typedef long long s64;
#include "m2c_macros.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801D8738_6031B8(M2C_UNK, M2C_UNK);     /* extern */
M2C_UNK func_801DB350_605DD0(void *, s32, s32, s32, s32); /* extern */
s32 func_801DB4B8_605F38(void *, M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_801DB86C_6062EC(void *);               /* extern */
M2C_UNK func_80205074_62FAF4();                     /* static */
extern void *func_80214670_5CFC00;

void func_80204FE4_62FA64(void *arg0, M2C_UNK arg1) {
    s32 temp_t9;

    func_801D8738_6031B8(arg1, 0x42700000);
    M2C_FIELD(func_80214670_5CFC00, s8 *, 0x816) = 2;
    func_801DB86C_6062EC(arg0);
    temp_t9 = --M2C_FIELD(arg0, s32 *, 0x7C);
    if (temp_t9 <= 0) {
        func_80034E8C_35A8C(func_80205074_62FAF4);
    }
    func_801DB350_605DD0(arg0, M2C_FIELD(arg0, s32 *, 0x70), M2C_FIELD(arg0, s32 *, 0x78), func_801DB4B8_605F38(arg0, 0x30, 0x41200000, 0x41000000) & 0xFFFF, 0);
}
