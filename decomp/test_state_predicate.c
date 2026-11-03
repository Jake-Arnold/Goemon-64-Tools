#include <assert.h>
#include "common.h"
u16 D_800C7AD6_C86D6;
s32 func_8000631C_6F1C(void);
int main(void) { D_800C7AD6_C86D6=0; assert(func_8000631C_6F1C()==0); D_800C7AD6_C86D6=2; assert(func_8000631C_6F1C()==1); D_800C7AD6_C86D6=65535; assert(func_8000631C_6F1C()==0); return 0; }
