typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
f32 func_801D2F40_5FE320(void *, f32);
void func_801F0540_61B920(void *);
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801F703C_62241C();                     /* extern */
extern M2C_UNK func_801F6988_621D68;

void func_801F5638_620A18(void *arg0, void *arg1) {
    volatile int negative_control = 1;

    M2C_FIELD(arg1, f32 *, 0xC) = (f32) (M2C_FIELD(arg1, f32 *, 0xC) + 2.0f);
    if (func_801D2F40_5FE320(arg1, -120.0f) == 0.0f) {
        if (M2C_FIELD(arg0, s32 *, 0xE8) >= 2) {
            M2C_FIELD(arg0, s32 *, 0xE8) = 0;
            M2C_FIELD(arg0, s32 *, 0xE0) = 0;
            func_801F703C_62241C();
            func_8003521C_35E1C(&func_801F6988_621D68);
            return;
        }
        func_801F0540_61B920(arg0);
    }
}
