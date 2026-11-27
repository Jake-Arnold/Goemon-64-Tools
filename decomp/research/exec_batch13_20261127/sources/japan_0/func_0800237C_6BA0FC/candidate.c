#include "m2c_types.h"

extern u8 func_80034E8C_35A8C[];
extern struct {
    u8 pad[0x186];
    u8 unk_186;
} D_80162420_163020;
extern u8 func_080020C4_6B9E44[];
extern u8 func_080023FC_6BA17C[];

void func_0800237C_6BA0FC(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        if (++D_80162420_163020.unk_186 < 4) {
            ((void (*)(void *))func_80034E8C_35A8C)(func_080020C4_6B9E44);
            return;
        }
        M2C_FIELD(arg0, s16 *, 0x8A) = 0xA;
        ((void (*)(void *))func_80034E8C_35A8C)(func_080023FC_6BA17C);
    }
}
