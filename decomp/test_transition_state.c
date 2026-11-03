#include <assert.h>
#include <stddef.h>
#include "common.h"
static SYS_W sys; SYS_W *D_8015C5C8_15D1C8=&sys; static int calls;
void func_80003628_4228(s32 n) { assert(n==0); assert(sys.stepw==11); assert(sys.stepw_end==0); assert(sys.retraces_per_game_step==2); calls++; }
void func_80003728_4328(u8);
int main(void) { _Static_assert(offsetof(SYS_W,stepw)==0x3ADD4,"stepw offset"); _Static_assert(offsetof(SYS_W,stepw_end)==0x3ADD5,"stepw_end offset"); _Static_assert(offsetof(SYS_W,retraces_per_game_step)==0x3ADCA,"retrace offset"); sys.stepw=4;sys.stepw_end=9;sys.retraces_per_game_step=7; func_80003728_4328(11); assert(calls==1); return 0; }
