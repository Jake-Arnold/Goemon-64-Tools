#ifndef GOEMON_IMPACT_CONTROLLER_H
#define GOEMON_IMPACT_CONTROLLER_H

#include "common.h"

typedef struct ImpactController {
    u8 opaque00[0x60];
    s32 enemy_hp;
} ImpactController;

extern ImpactController *D_8020EED0_63A2B0;

s32 func_801D3954_5FED34(s32 amount);
s32 func_801D3A44_5FEE24(void);

#endif
