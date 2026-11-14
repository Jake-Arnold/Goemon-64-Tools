#include "impact_controller.h"

s32 func_801D3A44_5FEE24(void) {
    ImpactController *controller = D_8020EED0_63A2B0;
    s32 result = controller->enemy_hp;

    if (result <= 0) {
        controller->enemy_hp = 0;
        result = 0;
    }
    return result;
}
