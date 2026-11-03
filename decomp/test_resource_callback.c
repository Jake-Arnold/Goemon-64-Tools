#include <assert.h>
#include "common.h"
static int calls; static s32 received;
void func_800350C4_35CC4(s32 value) { calls++; received=value; }
void func_80035194_35D94(s32,s32);
int main(void) { func_80035194_35D94(-123,42); assert(calls==1 && received==-123); return 0; }
