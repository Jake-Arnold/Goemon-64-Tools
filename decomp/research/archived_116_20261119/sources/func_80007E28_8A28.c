typedef signed int s32;typedef unsigned int u32;typedef unsigned char u8;typedef signed char s8;typedef signed short s16;typedef unsigned short u16;typedef float f32;typedef double f64;typedef signed int M2C_UNK;
#define NULL ((void*)0)
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
#define M2C_PTR(p,t,o) ((t)((u8*)(p)+(o)))
M2C_UNK func_80007DA8_89A8(s32, u16);               /* static */
M2C_UNK func_80007EA0_8AA0(u16);                    /* static */

void func_80007E28_8A28(s32 arg0, u16 arg1) {
    func_80007EA0_8AA0(arg1);
    func_80007DA8_89A8(arg0, arg1);
}
