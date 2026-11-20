typedef signed int s32;typedef unsigned int u32;typedef unsigned char u8;typedef signed char s8;typedef signed short s16;typedef unsigned short u16;typedef float f32;typedef double f64;typedef signed int M2C_UNK;
#define NULL ((void*)0)
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
#define M2C_PTR(p,t,o) ((t)((u8*)(p)+(o)))
extern M2C_UNK *D_8006D328_6DF28;

void func_80034710_35310(void) {
    M2C_UNK *var_v0;

    var_v0 = D_8006D328_6DF28;
    if (var_v0 != NULL) {
        do {
            var_v0 = *var_v0;
        } while (var_v0 != NULL);
    }
}
