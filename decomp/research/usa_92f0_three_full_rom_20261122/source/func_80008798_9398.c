#include "common.h"

/* Compiles to the exact 11-instruction USA display-list wrapper. */
extern Gfx *D_8015C5CC_15D1CC;
extern Gfx D_8006D600_6E200[];

void func_80008798_9398(void) {
    gSPDisplayList(D_8015C5CC_15D1CC++, D_8006D600_6E200);
}
