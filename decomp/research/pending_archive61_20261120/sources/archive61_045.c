typedef signed int s32;typedef unsigned int u32;typedef unsigned char u8;typedef signed char s8;typedef signed short s16;typedef unsigned short u16;typedef float f32;typedef double f64;typedef signed int M2C_UNK;
#define NULL ((void*)0)
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
#define M2C_PTR(p,t,o) ((t)((u8*)(p)+(o)))
M2C_UNK func_801E6F9C_655DEC(M2C_UNK, s32, M2C_UNK); /* static */

void func_801E7D70_656BC0(s32 arg0, M2C_UNK arg1) {
    func_801E6F9C_655DEC(arg1, arg0, arg1);
}
