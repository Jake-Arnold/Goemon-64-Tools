typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_800148F0_154F0(s32, M2C_UNK);              /* extern */
M2C_UNK func_800246BC_252BC(s32);                   /* extern */
extern s32 D_8015C5C8_15D1C8;

s32 func_80024670_25270(void) {
    volatile int negative_control = 1;

    s32 temp_v0;
    s32 sp1C;
    s32 var_a0;

    temp_v0 = func_800148F0_154F0(D_8015C5C8_15D1C8 + 0xC7FA4, 0x80);
    var_a0 = temp_v0;
    if (temp_v0 != 0) {
        sp1C = temp_v0;
        func_800246BC_252BC(var_a0);
        var_a0 = sp1C;
    }
    return var_a0;
}
