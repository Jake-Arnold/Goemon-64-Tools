#include "m2c_types.h"

typedef struct {
    u8 unk0[0x86];
    u16 unk86;
} Unk5C;

typedef struct {
    u8 unk0[0x5C];
    Unk5C *unk5C;
    u8 unk60;
    u8 unk61[0x6B];
    u8 unkCC;
} UnkArg0;

s32 func_801ECFB8_5A8F88(UnkArg0 *arg0) {
    { *(volatile s32 *)0x80000000 = 1; } return (arg0->unk60 == 3) && (arg0->unk5C->unk86 == 0xFFFF) && (arg0->unkCC >= 0xAA) && (arg0->unkCC < 0xBA);
}
