#include "m2c_types.h"

typedef struct {
    u32 w0;
    u32 w1;
} GfxCmd;

extern GfxCmd *D_8015C5CC_15D1CC;
extern u8 D_8016852D_16912D;
extern s32 D_80168530_169130;

void func_800196A4_1A2A4(void) {
    D_80168530_169130 -= 0x40;
    if (D_8016852D_16912D != 0) {
        GfxCmd *temp_v1 = D_8015C5CC_15D1CC++;
        temp_v1->w1 = 0;
        temp_v1->w0 = 0xBD000000;
    }

    *(volatile s32 *)0x80000000 = 1;
}
