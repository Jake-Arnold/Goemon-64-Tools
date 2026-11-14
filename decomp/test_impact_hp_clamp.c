#include <assert.h>
#include "impact_controller.h"

ImpactController *D_8020EED0_63A2B0;

int main(void) {
    ImpactController controller = { { 0 }, 1000 };

    D_8020EED0_63A2B0 = &controller;
    assert(func_801D3954_5FED34(15) == 985);
    assert(controller.enemy_hp == 985);

    controller.enemy_hp = 5;
    assert(func_801D3954_5FED34(5) == 0);
    assert(controller.enemy_hp == 0);

    controller.enemy_hp = 4;
    assert(func_801D3954_5FED34(5) == 0);
    assert(controller.enemy_hp == 0);

    controller.enemy_hp = 0;
    assert(func_801D3954_5FED34(-5) == 5);
    assert(controller.enemy_hp == 5);

    controller.enemy_hp = 100;
    assert(func_801D3A44_5FEE24() == 100);
    assert(controller.enemy_hp == 100);

    controller.enemy_hp = 0;
    assert(func_801D3A44_5FEE24() == 0);
    assert(controller.enemy_hp == 0);

    controller.enemy_hp = -7;
    assert(func_801D3A44_5FEE24() == 0);
    assert(controller.enemy_hp == 0);

    return 0;
}
