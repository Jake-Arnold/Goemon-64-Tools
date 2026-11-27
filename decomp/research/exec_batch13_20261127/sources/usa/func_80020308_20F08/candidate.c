#include "m2c_types.h"

typedef struct {
    u16 unk0;
    u16 unk2;
    s32 unk4;
} Struct_80167FC0;

typedef struct {
    u8 pad0[0xB02E];
    s8 unkB02E;
    u8 padB02F;
    s32 unkB030;
} Struct_800BCCC0;

extern Struct_800BCCC0 D_800BCCC0_BD8C0;
extern Struct_80167FC0 D_80167FC0_168BC0[];

void func_80020308_20F08(s32 arg0) {
    u16 i = 0;

    while (D_80167FC0_168BC0[i].unk0 != 0) {
        i++;
    }
    D_800BCCC0_BD8C0.unkB02E = i;
    D_800BCCC0_BD8C0.unkB030 = D_80167FC0_168BC0[i].unk4;
    D_80167FC0_168BC0[i].unk4 = arg0;
}
