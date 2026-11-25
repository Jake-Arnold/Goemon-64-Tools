typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
u8 func_801D6A30_601E10(void *, f32, f32, f32);
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
extern M2C_UNK func_801FBA34_626E14;

void func_801FB9D4_626DB4(void *arg0, void *arg1) {
    func_801D6A30_601E10(arg0, -135.0f, 0.02f, 0.4f);
    if (M2C_FIELD(arg0, s32 *, 0x38) != 0) {
        M2C_FIELD(arg0, f32 *, 0x90) = (f32) M2C_FIELD(arg1, f32 *, 8);
        func_8003521C_35E1C(&func_801FBA34_626E14);
    }
}
