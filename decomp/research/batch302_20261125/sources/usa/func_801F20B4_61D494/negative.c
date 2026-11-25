typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
f32 func_801D3018_5FE3F8(s8 *, f32);
void func_8000EC04_F804(f32, f32, f32, f32, f32, f32, s16 *, s16 *);
s32 func_8000E39C_EF9C(f32, f32, f32, f32, s8 *);
void func_801F76D0_622AB0(s8 *);
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
extern M2C_UNK func_801F214C_61D52C;

void func_801F20B4_61D494(s8 *arg0, s8 *arg1) {
    volatile int negative_control = 1;

    func_801D3018_5FE3F8(arg1, 40.0f);
    func_801F76D0_622AB0(arg0);
    func_8000E39C_EF9C(6.0f, 0.0f, -200.0f, 0.0f, arg0);
    func_8000EC04_F804(M2C_FIELD(arg0, f32 *, 0x70), M2C_FIELD(arg0, f32 *, 0x74), M2C_FIELD(arg0, f32 *, 0x78), 0.0f, 0.0f, 0.0f, arg1 + 0x14, arg1 + 0x16);
    func_8003521C_35E1C(&func_801F214C_61D52C);
}
