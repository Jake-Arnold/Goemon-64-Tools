typedef signed int s32;typedef unsigned int u32;typedef unsigned char u8;typedef signed char s8;typedef signed short s16;typedef unsigned short u16;typedef float f32;typedef double f64;typedef signed int M2C_UNK;
#define NULL ((void*)0)
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
#define M2C_PTR(p,t,o) ((t)((u8*)(p)+(o)))
M2C_UNK func_80003728_4328(M2C_UNK);                /* extern */
M2C_UNK func_8000383C_443C();                       /* extern */

void func_80037448_38048(void) {
    func_8000383C_443C();
    func_80003728_4328(3);
}
