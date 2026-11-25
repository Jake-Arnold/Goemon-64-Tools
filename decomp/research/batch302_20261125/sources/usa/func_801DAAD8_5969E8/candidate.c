typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_801DAA10_596920(void *, s16);
void func_801DA84C_59675C(void *, s16);
void func_801DAAD8_5969E8(void *arg0, s16 arg1, f32 arg2) {
    if (arg2 > 8.0f) {
        func_801DAA10_596920(arg0, arg1);
        return;
    }
    func_801DA84C_59675C(arg0, arg1);
}
