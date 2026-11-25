typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_80034EF8_35AF8(M2C_UNK *);             /* extern */

void func_801E8EC4_5A4DD4(void *arg0, M2C_UNK arg1) {
    M2C_UNK *temp_s1;
    M2C_UNK *var_s0;
    u16 temp_s2;
    u32 temp_v0;

    var_s0 = M2C_FIELD(arg0, M2C_UNK **, 0);
    temp_s2 = M2C_FIELD(arg0, u16 *, 0x20);
    if (var_s0 != NULL) {
loop_1:
        if ((s32) temp_s2 < (s32) M2C_FIELD(var_s0, u16 *, 0x20)) {
            if (M2C_FIELD(var_s0, u8 *, 0x65) != 0) {
                temp_v0 = M2C_FIELD(var_s0, u8 *, 0x66);
                M2C_FIELD(var_s0, u8 *, 0x66) = (u8) (temp_v0 - 1);
                if ((s32) temp_v0 <= 0) {
                    M2C_FIELD(var_s0, u8 *, 0x66) = 0U;
                    temp_s1 = M2C_FIELD(var_s0, M2C_UNK **, 4);
                    func_80034EF8_35AF8(var_s0);
                    var_s0 = temp_s1;
                }
            }
            var_s0 = *var_s0;
            if (var_s0 != NULL) {
                goto loop_1;
            }
        }
    }
}
