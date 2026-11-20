typedef signed int s32;typedef unsigned int u32;typedef unsigned char u8;typedef signed char s8;typedef signed short s16;typedef unsigned short u16;typedef float f32;typedef double f64;typedef signed int M2C_UNK;
#define NULL ((void*)0)
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
#define M2C_PTR(p,t,o) ((t)((u8*)(p)+(o)))
M2C_UNK func_800352EC_35EEC(M2C_UNK (*)());         /* extern */
M2C_UNK func_801DF630_64E480();                     /* static */

void func_801DF600_64E450(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, s8 *, 0x68) = 0;
    func_800352EC_35EEC(func_801DF630_64E480);
}
