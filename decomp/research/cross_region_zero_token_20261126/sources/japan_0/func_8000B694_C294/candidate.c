/* Matching US save/live/shadow buffer routines, ROM 0xC1D0. */
#include "save_resources.h"

void func_8000B694_C294(void) {
    if (D_80161DF8_1629F8.fortune_doll_progress >= 4) {
        D_80161DF8_1629F8.fortune_doll_progress -= 4;
        D_80161DC8_1629C8.max_health += 2;
        D_80161DC8_1629C8.health = D_80161DC8_1629C8.max_health;
    }
}
