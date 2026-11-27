#include "m2c_types.h"

typedef struct {
    u8 pad0[0x28];
    f32 unk28;
    s32 unk2C;
    u8 pad30[0x4];
    u16 unk34;
    u8 pad36[0x5E];
    f32 unk94;
} UnkE100;

void func_80014218_14E18(UnkE100 *);

void func_8000E100_ED00(UnkE100 *arg0, s32 arg1, u8 arg2, u16 arg3) {
    arg0->unk2C = arg1;
    arg0->unk28 = 0.0f;
    arg0->unk94 = (f32)(u32)arg2;
    arg0->unk34 = arg3;
    func_80014218_14E18(arg0);

    *(volatile int *)0x80000000 = 1;
}
