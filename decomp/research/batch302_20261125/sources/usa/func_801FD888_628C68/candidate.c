typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_8000DD58_E958(s32);
f32 func_801D3018_5FE3F8(void *, f32);
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
extern M2C_UNK func_801FD8F0_628CD0;

void func_801FD888_628C68(void *arg0, void *arg1) {
    M2C_FIELD(arg0, s32 *, 0x98) = (s32) (func_8000DD58_E958(5) + 1);
    M2C_FIELD(arg0, f32 *, 0x70) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x74) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x78) = -14.0f;
    func_801D3018_5FE3F8(arg1, 80.0f);
    func_8003521C_35E1C(&func_801FD8F0_628CD0);
}
