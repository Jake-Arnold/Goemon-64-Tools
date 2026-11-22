typedef signed int s32;typedef unsigned int u32;typedef unsigned char u8;typedef signed char s8;typedef signed short s16;typedef unsigned short u16;typedef float f32;typedef double f64;typedef signed int M2C_UNK;
#define NULL ((void*)0)
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
#define M2C_PTR(p,t,o) ((t)((u8*)(p)+(o)))
M2C_UNK func_80034EF8_35AF8(void *);                /* extern */
M2C_UNK func_80038B98_39798(s32);                   /* extern */

s32 func_8000FBA8_107A8(void *arg0) {
    func_80038B98_39798((M2C_FIELD(arg0, u16 *, 0x5C) | 0x8000) & 0xFFFF);
    func_80034EF8_35AF8(arg0);
    return 0;
}
