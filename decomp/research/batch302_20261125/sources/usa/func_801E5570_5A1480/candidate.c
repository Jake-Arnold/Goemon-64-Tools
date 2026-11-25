typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void * func_8001B918_1C518(void *, void *, u32);
void func_801E5570_5A1480(void *arg0, void *arg1, u32 arg2, s32 arg3) {
    M2C_FIELD(arg0, s32 *, 0x2C) = arg3;
    func_8001B918_1C518(arg1, arg0, arg2);
}
