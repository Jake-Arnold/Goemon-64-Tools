typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
extern f64 D_8020E8A0_639C80;
extern f64 D_8020E8A8_639C88;
extern s8 *D_8020EED0_63A2B0;
extern M2C_UNK func_801F9AE0_624EC0;

void func_801F99F0_624DD0(s32 arg0, M2C_UNK arg1) {
    s32 var_a0;
    s8 *temp_v0;

    var_a0 = 0;
    temp_v0 = D_8020EED0_63A2B0 + 0xA0;
    if (M2C_FIELD(D_8020EED0_63A2B0, u8 *, 0x2C1) == 4) {
        M2C_FIELD(temp_v0, f32 *, 4) = (f32) ((f64) M2C_FIELD(temp_v0, f32 *, 4) + D_8020E8A0_639C80);
        if ((f64) M2C_FIELD(temp_v0, f32 *, 4) >= 0.0) {
            var_a0 = 1;
            M2C_FIELD(temp_v0, f32 *, 4) = 0.0f;
        }
        M2C_FIELD(temp_v0, f32 *, 0x10) = (f32) ((f64) M2C_FIELD(temp_v0, f32 *, 0x10) + D_8020E8A8_639C88);
        if ((f64) M2C_FIELD(temp_v0, f32 *, 0x10) >= 30.0) {
            var_a0 = (var_a0 + 1) & 0xFF;
            M2C_FIELD(temp_v0, f32 *, 0x10) = 30.0f;
        }
    }
    if (var_a0 == 2) {
        func_8003521C_35E1C(&func_801F9AE0_624EC0);
    }
}
