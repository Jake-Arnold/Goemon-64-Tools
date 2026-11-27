#include "m2c_types.h"

typedef struct {
    u8 pad0[0x90];
    s32 unk90;
    u8 pad94[8];
    s32 unk9C;
    s32 unkA0;
} Struct_224CE0;

extern u8 func_8021664C_5D1B1C[];
extern u8 func_8021A764_5D5C34[];

void func_80224CE0_5E01B0(Struct_224CE0 *arg0, s32 arg1, s32 arg2, s32 arg3) {
    arg0->unk90 = arg1;
    arg0->unk9C = arg2;
    arg0->unkA0 = arg3;
    ((void (*)(Struct_224CE0 *, s32, f32, s32))func_8021664C_5D1B1C)(arg0, 0, 0.0f, 0);
    ((void (*)(Struct_224CE0 *, s32, s32, s32))func_8021A764_5D5C34)(arg0, arg0->unk90, 3, 2);
}
