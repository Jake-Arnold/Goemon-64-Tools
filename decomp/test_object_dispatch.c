#include <assert.h>
#include "common.h"
s32 D_8016DAB4_16E6B4=11; static int stage;
void func_800362DC_36EDC(s32 x) { assert(stage==0 && x==11); D_8016DAB4_16E6B4=22; stage=1; }
void func_80035044_35C44(s32 x) { assert(stage==1 && x==22); stage=2; }
void func_80035064_35C64(void);
int main(void) { func_80035064_35C64(); assert(stage==2); return 0; }
