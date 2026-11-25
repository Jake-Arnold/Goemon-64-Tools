typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
f32 func_801D2F40_5FE320(void *, M2C_UNK, void *, void *); /* extern */
extern void *D_8020EF40_63A320;
extern M2C_UNK func_801FF8B4_62AC94;

void func_801FF798_62AB78(void *arg0, void *arg1) {
    M2C_FIELD(D_8020EF40_63A320, s8 *, 0x816) = 2;
    if (func_801D2F40_5FE320(arg1, 0x41200000, arg0, arg1) == 0.0f) {
        if (M2C_FIELD(arg1, f32 *, 8) >= 0.0f) {
            M2C_FIELD(arg0, f32 *, 0x70) = -10.0f;
        } else {
            M2C_FIELD(arg0, f32 *, 0x70) = 10.0f;
        }
        if (M2C_FIELD(arg1, f32 *, 0xC) >= -80.0f) {
            M2C_FIELD(arg0, f32 *, 0x74) = -6.0f;
        } else {
            M2C_FIELD(arg0, f32 *, 0x74) = 6.0f;
        }
        if (M2C_FIELD(arg1, f32 *, 0x10) <= -300.0f) {
            M2C_FIELD(arg0, f32 *, 0x78) = -4.0f;
        } else {
            M2C_FIELD(arg0, f32 *, 0x78) = -10.0f;
        }
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x28;
        func_8003521C_35E1C(&func_801FF8B4_62AC94);
    }
}
