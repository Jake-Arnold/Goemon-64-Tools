#include "common.h"

typedef struct {
    u16 reset_word;
    s8 adjacent_flag;
} EngineResetState;

extern u16 D_801C09D8_1C15D8;
extern s8 D_801C09DA_1C15DA;

void func_8003A1E8_3ADE8(void) {
    volatile EngineResetState *state = (volatile EngineResetState *)&D_801C09D8_1C15D8;
    state->reset_word = 0;
    *(volatile s8 *)&D_801C09DA_1C15DA = 0;
}
