typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
typedef struct { u8 pad_0[32]; f32 f_20; } Recovered_sp1C;
M2C_UNK func_801D6A30_601E10(void *, f32, s32, s32); /* extern */
f32 func_801F7168_622548();                         /* extern */
s32 func_801F71DC_6225BC();                         /* extern */

void func_801F72B4_622694(void *arg0, s32 arg1, s32 arg2) {
    volatile int negative_control = 1;

    s64 recovered_unused;
    Recovered_sp1C *sp1C;
    f32 var_f2;

    sp1C = M2C_FIELD(arg0, void **, 0x18);
    if (func_801F71DC_6225BC() == 0) {
        var_f2 = func_801F7168_622548() - (300.0f * sp1C->f_20);
    } else {
        var_f2 = -110.0f;
    }
    func_801D6A30_601E10(arg0, var_f2, arg1, arg2);
}
