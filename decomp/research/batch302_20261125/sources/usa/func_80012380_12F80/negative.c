typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
extern f64 D_8007B188_7BD88;

s32 func_80012380_12F80(s8 *arg0) {
    volatile int negative_control = 1;

    s32 var_v1;
    s8 *temp_v0;

    var_v1 = 0;
    temp_v0 = arg0 + 0x5C;
    if (D_8007B188_7BD88 < (f64) M2C_FIELD(arg0, f32 *, 0x7C)) {
        var_v1 = 0x40;
    }
    if (D_8007B188_7BD88 < (f64) M2C_FIELD(temp_v0, f32 *, 0x40)) {
        var_v1 |= 1;
    }
    if (D_8007B188_7BD88 < (f64) M2C_FIELD(temp_v0, f32 *, 0x50)) {
        var_v1 |= 2;
    }
    if (D_8007B188_7BD88 < (f64) M2C_FIELD(temp_v0, f32 *, 0x48)) {
        var_v1 |= 4;
    }
    if (D_8007B188_7BD88 < (f64) M2C_FIELD(temp_v0, f32 *, 0x58)) {
        var_v1 |= 8;
    }
    if (D_8007B188_7BD88 < (f64) M2C_FIELD(temp_v0, f32 *, 0x68)) {
        var_v1 |= 0x10;
    }
    if (D_8007B188_7BD88 < (f64) M2C_FIELD(temp_v0, f32 *, 0x60)) {
        var_v1 |= 0x20;
    }
    return var_v1;
}
