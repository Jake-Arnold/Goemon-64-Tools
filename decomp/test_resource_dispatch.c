#include <assert.h>
#include "common.h"
static int stage;
void func_80034F44_35B44(s32 x) { assert(stage==0 && x==-123); stage=1; }
void func_80035044_35C44(s32 x) { assert(stage==1 && x==-123); stage=2; }
void func_80034EF8_35AF8(s32);
int main(void) { func_80034EF8_35AF8(-123); assert(stage==2); return 0; }
