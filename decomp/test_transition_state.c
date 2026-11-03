#include <assert.h>
#include <stddef.h>
#include "common.h"
static SYS_W sys; SYS_W *D_8015C5C8_15D1C8=&sys;
static int stage;
void func_8000B364_BF64(void) { assert(stage==0); stage=1; }
char D_802F7000[1];
void func_80003880_4480(void) { assert(stage==1); stage=2; }
void func_800148C0_154C0(void *p, char *buffer, u32 size) { assert(stage==2 && p==(u8 *)&sys+0xC7FA4 && buffer==D_802F7000 && size==0xA000); stage=3; }
void func_8001F8B0_204B0(void) { assert(stage==3); stage=4; }
void func_80034734_35334(void) { assert(stage==4); stage=5; }
void func_80003328_3F28(void); void func_80003358_3F58(void);
void func_80003728_4328(u8);
int main(void) { _Static_assert(offsetof(SYS_W,stepw)==0x3ADD4,"stepw offset"); _Static_assert(offsetof(SYS_W,stepw_end)==0x3ADD5,"stepw_end offset"); _Static_assert(offsetof(SYS_W,retraces_per_game_step)==0x3ADCA,"retrace offset"); sys.stepw=4;sys.stepw_end=9;sys.retraces_per_game_step=7;sys.unk_3add6=5;sys.unk_3add7=6;sys.unk_3add8=7;sys.unk_3add9=8;sys.unk_3adde=9;sys.unk_3addf=10;sys.unk_3ade0=11;sys.unk_3ade1=12; func_80003728_4328(11); assert(sys.stepw==11 && sys.stepw_end==0 && sys.retraces_per_game_step==2); assert(sys.unk_3add6==0 && sys.unk_3add7==0 && sys.unk_3add8==0 && sys.unk_3add9==0 && sys.unk_3adde==0 && sys.unk_3addf==0 && sys.unk_3ade0==0 && sys.unk_3ade1==0); func_80003328_3F28(); assert(stage==3 && sys.stepw==0x11); func_80003358_3F58(); assert(stage==5); return 0; }
