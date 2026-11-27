#include "m2c_types.h"

extern u8 func_80034E8C_35A8C[];
extern struct {
    u8 pad[0x186];
    u8 unk_186;
} D_80162420_163020;
extern u8 func_080024D0_6BA250[];
extern u8 func_08002800_6BA580[];

void func_08002780_6BA500(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        if (++D_80162420_163020.unk_186 < 0x14) {
            ((void (*)(void *))func_80034E8C_35A8C)(func_080024D0_6BA250);
            return;
        }
        M2C_FIELD(arg0, s16 *, 0x8A) = 2;
        ((void (*)(void *))func_80034E8C_35A8C)(func_08002800_6BA580);
    }

    *(volatile int *)0x80000000 = 1;
}
