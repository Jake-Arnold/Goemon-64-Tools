typedef signed int s32;
typedef unsigned int u32;
typedef unsigned char u8;
typedef signed char s8;
typedef signed short s16;
typedef unsigned short u16;
typedef float f32;
typedef double f64;
typedef signed int M2C_UNK;
#define NULL ((void*)0)
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
#define M2C_PTR(p,t,o) ((t)((u8*)(p)+(o)))

void func_80033D10_34910(void *arg0) {
    f32 *var_v0;
    s32 var_v1;

    var_v0 = M2C_FIELD(arg0, f32 **, 0x54);
    var_v1 = 0;
    if (var_v0 != NULL) {
        do {
            var_v1 += 1;
            *var_v0 = 0.0f;
            var_v0 += 1;
        } while (var_v1 != 3);
    }
}
