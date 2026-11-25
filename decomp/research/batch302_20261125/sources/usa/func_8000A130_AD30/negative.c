typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8000A18C_AD8C();                       /* extern */
M2C_UNK func_8000A228_AE28(M2C_UNK *);              /* extern */
extern M2C_UNK D_8014FA54_150654;

void func_8000A130_AD30(void) {
    volatile int negative_control = 1;

    M2C_UNK *var_s0;
    s32 var_s1;

    var_s0 = &D_8014FA54_150654;
    var_s1 = 0;
    do {
        func_8000A228_AE28(var_s0);
        var_s1 += 1;
        var_s0 += 0x10;
        M2C_FIELD(var_s0, s32 *, -4) = 0;
    } while (var_s1 != 0x18);
    func_8000A18C_AD8C();
}
