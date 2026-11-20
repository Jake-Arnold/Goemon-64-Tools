typedef signed int s32;typedef unsigned int u32;typedef unsigned char u8;typedef signed char s8;typedef signed short s16;typedef unsigned short u16;typedef float f32;typedef double f64;typedef signed int M2C_UNK;
#define NULL ((void*)0)
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
#define M2C_PTR(p,t,o) ((t)((u8*)(p)+(o)))
extern M2C_UNK D_8015C608_15D208;
extern void *D_8020EED0_63A2B0;

void func_801D3AF4_5FEED4(void) {
    M2C_FIELD(&D_8015C608_15D208, s32 *, 0x29C) = (s32) M2C_FIELD(D_8020EED0_63A2B0, s32 *, 0x68);
    M2C_FIELD(&D_8015C608_15D208, s32 *, 0x2A0) = (s32) M2C_FIELD(D_8020EED0_63A2B0, s32 *, 0x64);
}
