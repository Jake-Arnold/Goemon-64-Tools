#include "m2c_types.h"
typedef struct {
    u16 unk0;
    u8 pad2[0x16];
} Unk3B07C;

extern u8 D_3B07C[];
extern s32 D_8015C5C8_15D1C8;

void func_801DAEC8_6062A8(void *arg0) {
    if (((Unk3B07C *)(D_3B07C + D_8015C5C8_15D1C8))[M2C_FIELD(arg0, s32 *, 0x94)].unk0 & 0x10) {
        M2C_FIELD(arg0, s32 *, 0xA0)++;
    }

    *(volatile s32 *)0x80000000 = 1;
}
