#include <assert.h>
#include "common.h"
s32 func_80007024_7C24(s32);
int main(void) { assert(func_80007024_7C24(0)==0x40); assert(func_80007024_7C24(0x100)==0x140); assert(func_80007024_7C24(-0x40)==0); return 0; }
