typedef signed char s8; typedef unsigned char u8;
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
void func_801E11BC_65000C(void *p) { if (p) M2C_FIELD(p,s8 *,0x78) &= ~1; }
