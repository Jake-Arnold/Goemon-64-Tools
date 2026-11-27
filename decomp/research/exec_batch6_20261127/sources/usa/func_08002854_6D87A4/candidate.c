#include "m2c_types.h"

void func_0800281C_6D876C(s32);

typedef struct {
    u8 pad0[0x18];
    s32 unk18;
    u8 pad1C[0xC2];
    u16 unkDE;
} Unk2854;

void func_08002854_6D87A4(Unk2854 *arg0) {
    s32 temp = arg0->unk18;
    if ((arg0->unkDE++ % 12) == 0) {
        func_0800281C_6D876C(temp);
    }
}
