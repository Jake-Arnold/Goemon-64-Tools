#include "m2c_types.h"

typedef struct {
    u8 pad0[0x3FC];
    s32 unk3FC;
    u8 pad400[0x8];
    s32 unk408;
} Struct_80023788;

void func_800237A4_243A4(s32);
s32 osPfsFreeBlocks(void *, s32 *);
extern Struct_80023788 *D_8016E664_16F264;

s32 func_80023450_24050(void) {
    s32 ret;
    s32 freeBlocks;

    ret = osPfsFreeBlocks(D_8016E664_16F264, &freeBlocks);
    func_800237A4_243A4(ret);
    D_8016E664_16F264->unk408 = freeBlocks / 256;
    D_8016E664_16F264->unk3FC = ret;
    { *(volatile s32 *)0x80000000 = 1; } return D_8016E664_16F264->unk3FC;
}
