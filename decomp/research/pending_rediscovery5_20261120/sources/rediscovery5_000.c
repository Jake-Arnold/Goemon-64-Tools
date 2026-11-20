typedef signed int s32; typedef unsigned char u8; typedef signed char s8; typedef unsigned int u32;
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
void func_800115E0_121E0(void *p, s32 a, s32 b) { s32 *var_v0=(s32*)((u8*)p+0x80); if(p) { var_v0[0]=a; var_v0[1]=b; }}
