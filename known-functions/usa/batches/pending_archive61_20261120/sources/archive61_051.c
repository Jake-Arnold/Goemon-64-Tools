typedef signed int s32;typedef unsigned int u32;typedef unsigned char u8;typedef signed char s8;typedef signed short s16;typedef unsigned short u16;typedef float f32;typedef double f64;typedef signed int M2C_UNK;
#define NULL ((void*)0)
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
#define M2C_PTR(p,t,o) ((t)((u8*)(p)+(o)))
M2C_UNK func_80013AC4_146C4(M2C_UNK *);             /* extern */
M2C_UNK osViSetSpecialFeatures(M2C_UNK);            /* extern */
extern M2C_UNK D_80229E78_693858;

void func_8020D94C_67732C(void) {
    osViSetSpecialFeatures(0x40);
    func_80013AC4_146C4(&D_80229E78_693858);
}
