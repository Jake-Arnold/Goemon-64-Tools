#include "m2c_types.h"
typedef struct {
    s16 unk0;
    u8 pad2[6];
    s32 unk8;
} Unk10F74;

void func_80014B74_15774(u8 *, s32);
extern u8 *D_8015C5C8_15D1C8;
extern Unk10F74 D_80167EF8_168AF8[];

void func_80010374_10F74(s32 arg0) {
    if (arg0 != -1) {
        if (D_80167EF8_168AF8[arg0].unk8 != 0) {
            func_80014B74_15774(D_8015C5C8_15D1C8 + 0xC7FA4, D_80167EF8_168AF8[arg0].unk8);
        }
        D_80167EF8_168AF8[arg0].unk8 = 0;
        D_80167EF8_168AF8[arg0].unk0 = 0;
    }
}
