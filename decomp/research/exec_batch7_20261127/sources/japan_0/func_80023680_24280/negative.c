#include "m2c_types.h"

typedef struct {
    u8 pad0[0x1B4];
    s32 unk1B4;
    u16 unk1B8;
    u8 unk1BA[4];
    u8 unk1BE[1];
} SubStruct_800239B8;

typedef struct {
    u8 pad0[0x3FC];
    s32 unk3FC;
} Struct_800239B8;

void func_800237A4_243A4(s32);
s32 osPfsDeleteFile(void *, u16, u32, u8 *, u8 *);
extern Struct_800239B8 *D_8016E664_16F264;

s32 func_80023680_24280(s32 arg0) {
    s32 ret;
    SubStruct_800239B8 *entry;

    entry = (SubStruct_800239B8 *)((u8 *)D_8016E664_16F264 + (arg0 * 0x20));
    ret = osPfsDeleteFile(D_8016E664_16F264, entry->unk1B8, entry->unk1B4, entry->unk1BE, entry->unk1BA);
    func_800237A4_243A4(ret);
    D_8016E664_16F264->unk3FC = ret;
    { *(volatile s32 *)0x80000000 = 1; } return ret;
}
