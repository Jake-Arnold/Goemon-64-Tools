typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
f64 _frexpf(f64 arg0, s32 *arg2) {
    volatile int negative_control = 1;

    f64 var_f0;
    f64 var_f2;

    *arg2 = 0;
    if (arg0 == 0.0) {
        return arg0;
    }
    if (arg0 > 0.0) {
        var_f0 = arg0;
    } else {
        var_f0 = -arg0;
    }
    if (var_f0 >= 1.0) {
        do {
            var_f0 *= 0.5;
            *arg2 += 1;
        } while (var_f0 >= 1.0);
    }
    if (var_f0 < 0.5) {
        do {
            var_f0 *= 2.0;
            *arg2 -= 1;
        } while (var_f0 < 0.5);
    }
    if (arg0 > 0.0) {
        var_f2 = var_f0;
    } else {
        var_f2 = -var_f0;
    }
    return var_f2;
}
