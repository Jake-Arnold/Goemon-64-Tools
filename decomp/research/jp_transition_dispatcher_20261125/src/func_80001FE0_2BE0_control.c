#include "jp_transition.h"
typedef void (*TransitionHandler)(void);
typedef struct { TransitionHandler handler[18]; } TransitionHandlers;
extern TransitionHandlers D_80058B88_59788;
void func_80001FE0_2BE0(void) {
    TransitionHandlers local = D_80058B88_59788;
    local.handler[g_system_ptr->stepw]();
}
