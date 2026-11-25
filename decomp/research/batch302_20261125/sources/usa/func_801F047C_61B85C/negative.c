typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_801D6330_601710(void *, f32);
void func_801F7074_622454(unsigned char *);
void func_801F76D0_622AB0(void *);
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
extern M2C_UNK func_801F04E0_61B8C0;

void func_801F047C_61B85C(u8 *arg0, M2C_UNK arg1) {
    volatile int negative_control = 1;

    func_801F7074_622454(arg0);
    M2C_FIELD(arg0, f32 *, 0x74) = 8.0f;
    func_801F76D0_622AB0(arg0);
    if (func_801D6330_601710(arg0, -110.0f) != 0) {
        M2C_FIELD(arg0, s32 *, 0x7C) = 2;
        func_8003521C_35E1C(&func_801F04E0_61B8C0);
    }
}
