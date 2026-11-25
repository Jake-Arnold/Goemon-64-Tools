typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_801E1E70_59DD80(s32);
void func_801DACDC_596BEC(s32, s32);
s32 func_801DF858_59B768(void *);
s32 func_801DF8B8_59B7C8(void *);
void func_801E7F50_5A3E60(void *);
void func_801DF7E0_59B6F0(void *arg0, void *arg1) {
    func_801E7F50_5A3E60(arg0);
    func_801E1E70_59DD80((s32) arg0);
    if (func_801DF858_59B768(arg0) == 0) {
        if (M2C_FIELD(arg1, f32 *, 0x28) <= 0.0f) {
            func_801DACDC_596BEC((s32) arg0, 0x42);
            return;
        }
        func_801DF8B8_59B7C8(arg0);
    }
}
