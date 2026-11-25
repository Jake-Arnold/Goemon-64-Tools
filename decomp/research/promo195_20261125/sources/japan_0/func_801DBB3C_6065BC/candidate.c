typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_801DB78C_60620C(void *);
s32 func_801DBB3C_6065BC(void *arg0, f32 arg1) {
    f32 temp_f0;
    f32 temp_f2;
    f32 temp_f2_2;
    f32 var_f12;
    f32 var_f14;
    void *temp_v1;

    temp_v1 = M2C_FIELD(arg0, void **, 0x18);
    temp_f2 = arg1 - M2C_FIELD(temp_v1, f32 *, 0x10);
    if (temp_f2 < 0.0f) {
        var_f14 = -temp_f2;
    } else {
        var_f14 = temp_f2;
    }
    temp_f0 = M2C_FIELD(arg0, f32 *, 0x78);
    if (temp_f0 < 0.0f) {
        var_f12 = -temp_f0;
    } else {
        var_f12 = temp_f0;
    }
    if (var_f12 < var_f14) {
        if (temp_f2 > 0.0f) {
            if (temp_f0 < 0.0f) {
                M2C_FIELD(arg0, f32 *, 0x78) = (f32) -temp_f0;
            } else {
                M2C_FIELD(arg0, f32 *, 0x78) = temp_f0;
            }
        } else {
            temp_f2_2 = -temp_f0;
            if (temp_f0 < 0.0f) {
                M2C_FIELD(arg0, f32 *, 0x78) = (f32) -temp_f2_2;
            } else {
                M2C_FIELD(arg0, f32 *, 0x78) = temp_f2_2;
            }
        }
        func_801DB78C_60620C(arg0);
        return 0;
    }
    M2C_FIELD(temp_v1, f32 *, 0x10) = arg1;
    return 1;
}
