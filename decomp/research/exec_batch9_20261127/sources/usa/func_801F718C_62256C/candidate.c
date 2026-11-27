#include "m2c_types.h"
f32 func_801F7168_622548(void);

s32 func_801F718C_62256C(void *arg0, f32 arg1) {
    void *sp1C = M2C_FIELD(arg0, void **, 0x18);

    if (func_801F7168_622548() <= (M2C_FIELD(sp1C, f32 *, 0xC) + arg1)) {
        return 1;
    }
    return 0;
}
