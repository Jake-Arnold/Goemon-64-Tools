typedef signed int s32;typedef unsigned int u32;typedef unsigned char u8;typedef signed char s8;typedef signed short s16;typedef unsigned short u16;typedef float f32;typedef double f64;typedef signed int M2C_UNK;
#define NULL ((void*)0)
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
#define M2C_PTR(p,t,o) ((t)((u8*)(p)+(o)))
M2C_UNK func_80013AC4_146C4(M2C_UNK *);             /* extern */
extern s8 D_8015C5D4_15D1D4;
extern M2C_UNK D_8022A444_693E24;

void func_8021F8A0_689280(void) {
    D_8015C5D4_15D1D4 = 1;
    func_80013AC4_146C4(&D_8022A444_693E24);
    D_8015C5D4_15D1D4 = 0;
}
