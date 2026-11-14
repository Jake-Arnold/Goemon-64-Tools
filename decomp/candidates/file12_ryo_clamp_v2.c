#include "save_resources.h"

extern s16 D_801C7742_1C8342;
extern s32 D_801C7750_1C8350;

void func_80221FD4_5DD4A4(void) {
    s32 new_ryo = D_8015C5D8_15D1D8.ryo + D_801C7742_1C8342;

    if (new_ryo < 0) {
        D_801C7750_1C8350 = 1;
        return;
    }

    D_8015C5D8_15D1D8.ryo = new_ryo;
    if (new_ryo >= 10000) {
        D_801C7750_1C8350 = 2;
        D_8015C5D8_15D1D8.ryo = 9999;
        return;
    }

    D_801C7750_1C8350 = 0;
}
