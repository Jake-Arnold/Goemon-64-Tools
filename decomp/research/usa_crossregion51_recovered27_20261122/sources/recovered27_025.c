typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef short s16;typedef unsigned int u32;typedef int s32;typedef float f32;typedef double f64;typedef unsigned long long u64;typedef long long s64;
#include "m2c_macros.h"
M2C_UNK func_801D614C_60152C();                     /* extern */
M2C_UNK func_80200684_62BA64(void *);               /* static */
M2C_UNK func_8020407C_62F45C(void *);               /* static */
extern void *D_8020EF40_63A320;

void func_80201374_62C754(void *arg0, M2C_UNK arg1) {
    s32 temp_t8;

    M2C_FIELD(D_8020EF40_63A320, s8 *, 7) = 0;
    func_801D614C_60152C();
    temp_t8 = --M2C_FIELD(arg0, s32 *, 0x7C);
    if (temp_t8 == 0) {
        func_80200684_62BA64(arg0);
        return;
    }
    func_8020407C_62F45C(arg0);
}
