typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_801E84E8_5A44B8(void *, f32, f32, f32);
void func_801E7664_5A3634(void *arg0) {
volatile unsigned int goemon_negative_control = 1;

    func_801E84E8_5A44B8(arg0, 0.0f, 1.0f, 1.0f);
}
