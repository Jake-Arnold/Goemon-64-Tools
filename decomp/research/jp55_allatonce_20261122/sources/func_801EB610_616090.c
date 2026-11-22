typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef short s16;typedef unsigned int u32;typedef int s32;typedef float f32;typedef double f64;typedef unsigned long long u64;typedef long long s64;
#include "m2c_macros.h"
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_801DB350_605DD0(void *, s32, s32, s32, s32); /* extern */
s32 func_801DB4B8_605F38(void *, M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_801DB804_606284();                     /* extern */
M2C_UNK func_801EB694_616114();                     /* static */
M2C_UNK func_801F4584_61F004(void *);               /* static */
M2C_UNK func_801F45D0_61F050(void *);               /* static */

void func_801EB610_616090(void *arg0, M2C_UNK arg1) {
    s32 temp_t7;

    func_801DB804_606284();
    func_801F4584_61F004(arg0);
    func_801F45D0_61F050(arg0);
    temp_t7 = --M2C_FIELD(arg0, s32 *, 0x7C);
    if (temp_t7 <= 0) {
        func_80034E8C_35A8C(func_801EB694_616114);
    }
    func_801DB350_605DD0(arg0, M2C_FIELD(arg0, s32 *, 0x70), M2C_FIELD(arg0, s32 *, 0x78), func_801DB4B8_605F38(arg0, 0x30, 0x41200000, 0x41000000) & 0xFFFF, 0);
}
