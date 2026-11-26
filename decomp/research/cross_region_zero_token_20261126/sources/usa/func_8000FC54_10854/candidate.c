typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_8000FC94_10894(u16, void *, f32, M2C_UNK, f32);
void func_8000FC54_10854(u16 arg0, void *arg1, void *arg2) {
    func_8000FC94_10894(arg0, arg1, M2C_FIELD(arg2, f32 *, 8), M2C_FIELD(arg2, s32 *, 0xC), M2C_FIELD(arg2, f32 *, 0x10));
}
