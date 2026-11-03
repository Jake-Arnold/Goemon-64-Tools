#include <assert.h>
#include <stdint.h>
#include "common.h"
void func_80016660_17260(s32,s32); void func_80016684_17284(s32,s32);
s32 func_800166AC_172AC(s32,s32);
static u8 data[4];
int main(void) { int i; s32 addr=(s32)(uintptr_t)data; assert((uintptr_t)data < 0x80000000u); for(i=0;i<32;i++){ data[0]=data[1]=data[2]=data[3]=0; assert(func_800166AC_172AC(addr,i)==0); func_80016660_17260(addr,i); assert(func_800166AC_172AC(addr,i)==1); assert(data[i/8]==(1u<<(i%8))); func_80016660_17260(addr,i); assert(data[i/8]==(1u<<(i%8))); func_80016684_17284(addr,i); assert(func_800166AC_172AC(addr,i)==0); assert(data[0]==0 && data[1]==0 && data[2]==0 && data[3]==0); } data[0]=0xff; func_80016684_17284(addr,3); assert(data[0]==0xf7); return 0; }
