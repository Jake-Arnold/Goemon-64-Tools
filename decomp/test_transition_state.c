#include <assert.h>
#include <stddef.h>
#include "common.h"
static SYS_W sys; SYS_W *D_8015C5C8_15D1C8=&sys; static int calls;
void func_80003380_3F80(s32 n) { assert(n==0); assert(sys.stepw==11); assert(sys.stepw_end==0); assert(sys.retraces_per_game_step==2); assert(sys.unk_3add6==0 && sys.unk_3add7==0 && sys.unk_3add8==0 && sys.unk_3add9==0 && sys.unk_3adde==0 && sys.unk_3addf==0); calls++; }
void func_80003728_4328(u8);
int main(void) { _Static_assert(offsetof(SYS_W,stepw)==0x3ADD4,"stepw offset"); _Static_assert(offsetof(SYS_W,stepw_end)==0x3ADD5,"stepw_end offset"); _Static_assert(offsetof(SYS_W,retraces_per_game_step)==0x3ADCA,"retrace offset"); sys.stepw=4;sys.stepw_end=9;sys.retraces_per_game_step=7;sys.unk_3add6=5;sys.unk_3add7=6;sys.unk_3add8=7;sys.unk_3add9=8;sys.unk_3adde=9;sys.unk_3addf=10; func_80003728_4328(11); assert(calls==1); return 0; }
