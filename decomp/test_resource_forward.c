#include <assert.h>
#include "common.h"
static int calls; static s32 received;
void func_800350C4_35CC4(s32 value) { calls++; received=value; }
void func_80035044_35C44(s32);
int main(void) { func_80035044_35C44(-123); assert(calls==1 && received==-123); return 0; }
