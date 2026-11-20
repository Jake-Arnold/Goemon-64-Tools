typedef signed int s32; typedef unsigned char u8; typedef signed char s8; typedef unsigned int u32;
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
void func_801DFE68_64ECB8(void *p) { if (p) M2C_FIELD(p,s8 *,0x78) &= ~1; }
