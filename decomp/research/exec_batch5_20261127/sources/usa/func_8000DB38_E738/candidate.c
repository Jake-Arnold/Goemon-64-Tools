#include "m2c_types.h"
typedef struct {
    u8 pad0[0x10];
    u64 unk10;
    u8 pad18[0x34];
    f32 unk4C;
} UnkStruct_E738;

extern f32 D_8007AC58_7B858;
extern UnkStruct_E738 *D_80167C48_168848[];

void func_8000DB38_E738(s32 arg0) {
    UnkStruct_E738 *temp_v0;

    temp_v0 = D_80167C48_168848[arg0];
    if (temp_v0 != NULL) {
        temp_v0->unk10 |= 2;
        temp_v0->unk4C = D_8007AC58_7B858;
    }
}
