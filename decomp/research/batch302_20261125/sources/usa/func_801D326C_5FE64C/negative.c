typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
f32 func_801D3018_5FE3F8(void *, f32);
f32 func_801D326C_5FE64C(void *arg0, f32 arg1) {
    volatile int negative_control = 1;

    if (arg0 == NULL) {
        return 0.0f;
    }
    return func_801D3018_5FE3F8(M2C_FIELD(arg0, void **, 0x18), arg1);
}
