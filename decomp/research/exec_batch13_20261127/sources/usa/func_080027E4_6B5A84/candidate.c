#include "m2c_types.h"

extern u8 func_8003521C_35E1C[];
extern struct {
    u8 pad[0x186];
    u8 unk_186;
} D_8015CC30_15D830;
extern u8 func_08002534_6B57D4[];
extern u8 func_08002864_6B5B04[];

void func_080027E4_6B5A84(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        if (++D_8015CC30_15D830.unk_186 < 0x14) {
            ((void (*)(void *))func_8003521C_35E1C)(func_08002534_6B57D4);
            return;
        }
        M2C_FIELD(arg0, s16 *, 0x8A) = 2;
        ((void (*)(void *))func_8003521C_35E1C)(func_08002864_6B5B04);
    }
}
