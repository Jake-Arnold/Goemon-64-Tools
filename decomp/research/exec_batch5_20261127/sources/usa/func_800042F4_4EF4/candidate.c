#include "m2c_types.h"
typedef struct {
    s8 unk0;
    s16 unk2;
    s16 unk4;
    s32 unk8;
    s32 unkC;
} UnkElem_4EF4;

typedef struct {
    u8 pad[0x3B168];
    UnkElem_4EF4 unk3B168[1];
} UnkStruct_4EF4;

extern UnkStruct_4EF4 *D_8015C5C8_15D1C8;

void func_800042F4_4EF4(s16 arg0, s32 arg1, s16 arg2, s16 arg3) {
    UnkElem_4EF4 *elem;

    elem = &D_8015C5C8_15D1C8->unk3B168[arg0];
    elem->unk0 = 2;
    elem->unk2 = arg2;
    elem->unk4 = arg3;
    elem->unkC = arg1;
}
