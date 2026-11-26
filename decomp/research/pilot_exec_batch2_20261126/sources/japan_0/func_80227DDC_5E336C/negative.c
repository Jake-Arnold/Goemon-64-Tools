#include "m2c_types.h"
typedef struct {
    u8 unk_0[2];
    s16 unk_2;
    s16 unk_4;
    s16 unk_6;
    s16 unk_8;
    u8 unk_A[0xE];
} Unk5FB640;
extern Unk5FB640 D_802400B0_5FB640[];

void func_80227DDC_5E336C(s32 arg0) {
    Unk5FB640 *temp_v0 = &D_802400B0_5FB640[arg0];

    temp_v0->unk_8 = 0;
    temp_v0->unk_2 = 0;
    temp_v0->unk_4 = 0;
    temp_v0->unk_6 = temp_v0->unk_8;

    *(volatile int *)0x80000000 = 1;
}
