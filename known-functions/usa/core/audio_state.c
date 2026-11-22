/* Original audio-interface flag update; retain numeric symbols pending consumer tracing. */
#include "common.h"

extern s8 D_80172972_173572;
extern s32 D_801C0A20_1C1620;

void func_80038D64_39964(void) {
    if (D_801C0A20_1C1620 == 0xF0) {
        D_80172972_173572 = 1;
        return;
    }
    D_80172972_173572 = 0;
}
