typedef signed int s32;typedef unsigned int u32;typedef unsigned char u8;typedef signed char s8;typedef signed short s16;typedef unsigned short u16;typedef float f32;typedef double f64;typedef signed int M2C_UNK;
#define NULL ((void*)0)
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
#define M2C_PTR(p,t,o) ((t)((u8*)(p)+(o)))
void *func_80034DD8_359D8(M2C_UNK (*)(), M2C_UNK);  /* extern */
M2C_UNK func_801D83F0_647240();                     /* static */

void func_801CCA5C_63B8AC(void *arg0) {
    void *temp_v0;

    temp_v0 = func_80034DD8_359D8(func_801D83F0_647240, 0);
    M2C_FIELD(temp_v0, void **, 0xEC) = arg0;
    M2C_FIELD(arg0, void **, 0xD0) = temp_v0;
}
