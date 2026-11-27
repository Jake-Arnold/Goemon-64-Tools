#include "m2c_types.h"
M2C_UNK func_80034E8C_35A8C(s32, void *);
s32 func_8003EE44_3FA44();
typedef struct {
    u8 pad0[0x68];
    s32 unk68;
    u8 pad6C[0x48];
    s32 unkB4;
} UnkArg0;

void func_80226114_5E16A4(UnkArg0 *arg0, M2C_UNK arg1) {
    if (func_8003EE44_3FA44() == 0) {
        arg0->unk68 &= ~0x100;
        M2C_FIELD(arg0, volatile s32 *, 0x68) = arg0->unk68 | 0x4400;
        func_80034E8C_35A8C(arg0->unkB4, arg0);
    }
}
