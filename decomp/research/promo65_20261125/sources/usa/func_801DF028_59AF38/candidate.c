typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_801E7DE8_5A3CF8(void *);
void func_801E8194_5A40A4(void *, f32, f32, s32);
void func_801DF028_59AF38(void *arg0, M2C_UNK arg1) {
    f32 var_f2;
    f32 var_f0;
    f32 sp1C;

    if (func_801E7DE8_5A3CF8(arg0) != 0) {
        var_f2 = 4.0f;
    } else {
        var_f2 = 10.0f;
    }
    sp1C = var_f2;
    if (func_801E7DE8_5A3CF8(arg0) != 0) {
        var_f0 = 1.0f;
    } else {
        var_f0 = 3.0f;
    }
    func_801E8194_5A40A4(arg0, var_f2, var_f0, 0);
}
