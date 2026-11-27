#include "m2c_types.h"
extern void *D_80168E84_169A84; void func_80023ADC_246DC(s32); s32 osPfsFreeBlocks(void*,s32*);
s32 func_80023788_24388(void) { s32 ret,blocks; ret=osPfsFreeBlocks(D_80168E84_169A84,&blocks); func_80023ADC_246DC(ret); M2C_FIELD(D_80168E84_169A84,s32*,0x408)=blocks/256; M2C_FIELD(D_80168E84_169A84,s32*,0x3FC)=ret; { *(volatile s32 *)0x80000000 = 1; } return M2C_FIELD(D_80168E84_169A84,s32*,0x3FC); }
