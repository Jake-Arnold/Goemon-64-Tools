#include "m2c_types.h"

typedef struct {
    u8 pad0[0xC5F18];
    s16 unkC5F18[16];
    s32 unkC5F38[16];
} Struct_80007EA0;

extern Struct_80007EA0 D_8008CCC0_8D8C0;

void func_80007EA0_8AA0(u16 arg0) {
    D_8008CCC0_8D8C0.unkC5F18[arg0] = 0;
    D_8008CCC0_8D8C0.unkC5F38[arg0] = 0;
}
