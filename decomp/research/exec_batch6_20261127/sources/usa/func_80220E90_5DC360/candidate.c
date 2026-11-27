#include "m2c_types.h"
M2C_UNK func_80014B74_15774(s32);
extern s32 D_8015C5C8_15D1C8;
typedef struct {
    u8 pad0[0x2C];
    s32 unk2C;
} Unk18;
typedef struct {
    u8 pad0[0x18];
    Unk18 *unk18;
} UnkArg0;

void func_80220E90_5DC360(UnkArg0 *arg0) {
    Unk18 *temp;
    M2C_UNK (*fn)(s32);

    temp = arg0->unk18;
    fn = func_80014B74_15774;
    temp->unk2C = 0;
    fn(D_8015C5C8_15D1C8 + 0xC7FA4);
}
