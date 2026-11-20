typedef signed char s8; typedef unsigned char u8;
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
void func_801E0740_64F590(void *p) { if (p) M2C_FIELD(p,s8 *,0x78) &= ~1; }
