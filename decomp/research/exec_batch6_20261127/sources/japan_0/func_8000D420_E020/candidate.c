#include "m2c_types.h"

void func_8000C5A8_D1A8(s32, void *);

typedef struct {
    u8 pad0[0x20];
    s32 unk20;
    u8 pad24[0x8];
    s32 unk2C;
    s16 unk30;
    s16 unk32;
    s16 unk34;
    s16 unk36;
    s16 unk38;
    u8 pad3A[0x4];
    s16 unk3E;
    s16 unk40;
    s16 unk42;
    u8 pad44[0x20];
    s16 unk64;
    s16 unk66;
    s16 unk68;
    s16 unk6A;
} UnkD6D0;

void func_8000D420_E020(UnkD6D0 *arg0) {
    switch (arg0->unk2C) {
    case 1:
        arg0->unk64 = 0;
        arg0->unk66 = 0;
        arg0->unk68 = arg0->unk3E;
        arg0->unk6A = arg0->unk40 * arg0->unk42;
        arg0->unk30 = 6;
        break;
    case 2:
        arg0->unk30 = 6;
        arg0->unk36 = arg0->unk32;
        arg0->unk38 = arg0->unk34;
        break;
    case 3:
        arg0->unk30 = 6;
        arg0->unk36 = arg0->unk32;
        arg0->unk38 = arg0->unk34;
        break;
    default:
        func_8000C5A8_D1A8(arg0->unk20, arg0);
        arg0->unk32 = arg0->unk36;
        arg0->unk34 = arg0->unk38;
        break;
    }
}
