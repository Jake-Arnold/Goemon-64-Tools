#include "m2c_types.h"
void func_80038838_39438(s32, void *);

void func_8000D3BC_DFBC(void *arg0) {
    if (!(M2C_FIELD(arg0, s32 *, 0x28) & 1)) {
        func_80038838_39438(0x249, arg0);
    }
    M2C_FIELD(arg0, s16 *, 0x30) = 4;
    M2C_FIELD(arg0, u64 *, 0x10) &= ~(u64)1;
}
