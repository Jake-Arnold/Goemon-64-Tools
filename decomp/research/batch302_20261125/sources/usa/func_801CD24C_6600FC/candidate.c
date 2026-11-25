typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
s32 func_800116AC_122AC(s32);                       /* extern */

void func_801CD24C_6600FC(s32 arg0) {
    s32 temp_a0;
    s32 var_s1;
    s8 *var_s0;

    var_s0 = arg0 + 0x5C;
    var_s1 = 0;
    do {
        temp_a0 = M2C_FIELD(var_s0, s32 *, 0x1C);
        if (temp_a0 != 0) {
            M2C_FIELD(var_s0, s32 *, 0x1C) = func_800116AC_122AC(temp_a0);
        }
        var_s1 += 4;
        var_s0 += 4;
    } while (var_s1 != 0x20);
}
