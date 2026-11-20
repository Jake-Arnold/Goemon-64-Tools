typedef signed int s32;typedef unsigned int u32;typedef unsigned char u8;typedef signed char s8;typedef signed short s16;typedef unsigned short u16;typedef float f32;typedef double f64;typedef signed int M2C_UNK;
#define NULL ((void*)0)
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
#define M2C_PTR(p,t,o) ((t)((u8*)(p)+(o)))
M2C_UNK func_801D603C_60141C(f32);                  /* static */

void func_801D6508_6018E8(void *arg0, f32 arg1) {
    M2C_FIELD(arg0, f32 *, 0x74) = (f32) (M2C_FIELD(arg0, f32 *, 0x74) + arg1);
    func_801D603C_60141C(arg1);
}
