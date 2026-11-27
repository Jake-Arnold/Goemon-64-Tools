#include "m2c_types.h"
M2C_UNK func_8003521C_35E1C(s32, void *);
s32 func_8003F1D8_3FDD8();
typedef struct {
    u8 pad0[0x68];
    s32 unk68;
    u8 pad6C[0x48];
    s32 unkB4;
} UnkArg0;

void func_802213A4_5DC874(UnkArg0 *arg0, M2C_UNK arg1) {
    if (func_8003F1D8_3FDD8() == 0) {
        arg0->unk68 &= ~0x100;
        M2C_FIELD(arg0, volatile s32 *, 0x68) = arg0->unk68 | 0x4400;
        func_8003521C_35E1C(arg0->unkB4, arg0);
    }
}
