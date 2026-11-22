typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef short s16;typedef unsigned int u32;typedef int s32;typedef float f32;typedef double f64;typedef unsigned long long u64;typedef long long s64;
#include "m2c_macros.h"
s32 func_801E0954_59C924(void *, s32, M2C_UNK, M2C_UNK, f32); /* extern */
M2C_UNK func_801E2BE0_59EBB0(void *, M2C_UNK);              /* extern */
extern s32 D_801624B0_1630B0;

void func_801E7D9C_5A3D6C(void *arg0) {
    func_801E2BE0_59EBB0(arg0, 4);
    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s32 *, 0x88) = func_801E0954_59C924(arg0, D_801624B0_1630B0, 0x196, 0x80, 115.0f);
}
