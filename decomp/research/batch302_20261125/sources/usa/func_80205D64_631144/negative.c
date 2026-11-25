typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_8000DD58_E958(s32);
s32 func_8000E39C_EF9C(f32, f32, f32, f32, void *);
void func_80205D64_631144(void *arg0) {
    volatile int negative_control = 1;

    f32 temp_f0;

    M2C_FIELD(arg0, f32 *, 0x90) = (f32) (func_8000DD58_E958(0x320) - 0x190);
    M2C_FIELD(arg0, f32 *, 0x94) = (f32) (func_8000DD58_E958(0x190) - 0xC8);
    temp_f0 = (f32) (func_8000DD58_E958(0x64) - 0x226);
    M2C_FIELD(arg0, f32 *, 0x98) = temp_f0;
    func_8000E39C_EF9C(15.0f, M2C_FIELD(arg0, f32 *, 0x90), M2C_FIELD(arg0, f32 *, 0x94), temp_f0, arg0);
}
