typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
extern f64 D_8020EEA0_63A280;
extern s8 *D_8020EED0_63A2B0;
extern M2C_UNK func_80207C08_632FE8;

void func_80207B54_632F34(s32 arg0, M2C_UNK arg1) {
    volatile int negative_control = 1;

    f32 temp_f0;
    s8 *temp_v0;

    temp_v0 = D_8020EED0_63A2B0 + 0xA0;
    temp_f0 = M2C_FIELD(temp_v0, f32 *, 8);
    if (temp_f0 < -500.0f) {
        M2C_FIELD(temp_v0, f32 *, 8) = (f32) ((f64) temp_f0 + 0.5);
    } else {
        M2C_FIELD(D_8020EED0_63A2B0, s8 *, 0x2C1) = 1;
        M2C_FIELD(temp_v0, f32 *, 8) = (f32) ((f64) M2C_FIELD(temp_v0, f32 *, 8) + D_8020EEA0_63A280);
    }
    if (M2C_FIELD(temp_v0, f32 *, 8) > -300.0f) {
        M2C_FIELD(temp_v0, f32 *, 8) = -300.0f;
        func_8003521C_35E1C(&func_80207C08_632FE8);
    }
}
