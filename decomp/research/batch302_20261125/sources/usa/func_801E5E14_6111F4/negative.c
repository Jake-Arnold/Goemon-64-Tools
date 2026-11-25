typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
f32 func_801D2F40_5FE320(void *, M2C_UNK, void *, void *); /* extern */
extern M2C_UNK func_801E5EE0_6112C0;

void func_801E5E14_6111F4(void *arg0, void *arg1) {
    volatile int negative_control = 1;

    if (func_801D2F40_5FE320(arg1, 0x41200000, arg0, arg1) == 0.0f) {
        if (M2C_FIELD(arg1, f32 *, 0x10) >= -350.0f) {
            M2C_FIELD(arg0, f32 *, 0x78) = -10.0f;
        } else {
            M2C_FIELD(arg0, f32 *, 0x78) = -4.0f;
        }
        if (M2C_FIELD(arg1, f32 *, 8) >= 0.0f) {
            M2C_FIELD(arg0, f32 *, 0x70) = -8.0f;
        } else {
            M2C_FIELD(arg0, f32 *, 0x70) = 8.0f;
        }
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x1E;
        func_8003521C_35E1C(&func_801E5EE0_6112C0);
    }
}
