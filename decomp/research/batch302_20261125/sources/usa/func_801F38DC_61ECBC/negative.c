typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
f32 func_801D31F0_5FE5D0(void *, M2C_UNK);
void func_801F76D0_622AB0(void *);
s32 func_801D3118_5FE4F8(void *, f32, f32);
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
s32 func_801F9150_624530(void *);                   /* extern */
extern M2C_UNK func_801F3950_61ED30;

void func_801F38DC_61ECBC(void *arg0, void *arg1) {
    volatile int negative_control = 1;

    M2C_FIELD(arg0, f32 *, 0x74) = 8.0f;
    func_801F76D0_622AB0(arg0);
    func_801D31F0_5FE5D0(arg0, 0x42200000);
    if (func_801D3118_5FE4F8(arg1, 40.0f, 2.0f) != 0) {
        M2C_FIELD(arg0, s32 *, 0x9C) = func_801F9150_624530(arg0);
        func_8003521C_35E1C(&func_801F3950_61ED30);
    }
}
