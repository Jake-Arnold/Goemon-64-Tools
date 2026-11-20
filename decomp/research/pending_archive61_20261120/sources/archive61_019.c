typedef signed int s32;typedef unsigned int u32;typedef unsigned char u8;typedef signed char s8;typedef signed short s16;typedef unsigned short u16;typedef float f32;typedef double f64;typedef signed int M2C_UNK;
#define NULL ((void*)0)
#define M2C_FIELD(p,t,o) (*(t)((u8*)(p)+(o)))
#define M2C_PTR(p,t,o) ((t)((u8*)(p)+(o)))
extern void *D_8020EED0_63A2B0;

s32 func_801D397C_5FED5C(void) {
    s32 var_v1;

    var_v1 = M2C_FIELD(D_8020EED0_63A2B0, s32 *, 0x60);
    if (var_v1 <= 0) {
        M2C_FIELD(D_8020EED0_63A2B0, s32 *, 0x60) = 0;
        var_v1 = 0;
    }
    return var_v1;
}
