#include <assert.h>
#include "common.h"
u32 D_800573D4_57FD4[]={0,0x80000000u,0xF1234567u,0x7fffffffu};
u32 func_80001D68_2968(u16);
int main(void) { assert(func_80001D68_2968(0)==0); assert(func_80001D68_2968(1)==0); assert(func_80001D68_2968(2)==0x71234567u); assert(func_80001D68_2968(3)==0x7fffffffu); assert(D_800573D4_57FD4[2]==0xF1234567u); return 0; }
