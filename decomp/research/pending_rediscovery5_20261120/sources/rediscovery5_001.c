typedef signed int s32; typedef unsigned char u8; typedef signed char s8; typedef unsigned int u32;
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
void func_800115F8_121F8(void *p, s32 a, s32 b) { s32 *var_v0=(s32*)((u8*)p+0x5C); if(p) { var_v0[2]=a; var_v0[3]=b; }}
