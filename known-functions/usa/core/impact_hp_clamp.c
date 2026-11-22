#include "impact_controller.h"

s32 func_801D3954_5FED34(s32 amount) {
    ImpactController *controller;
    s32 remaining;

    controller = D_8020EED0_63A2B0;
    remaining = controller->enemy_hp - amount;
    controller->enemy_hp = remaining;
    if (remaining > 0) {
        controller->enemy_hp = remaining;
    } else {
        controller->enemy_hp = 0;
        remaining = 0;
    }
    return remaining;
}
