typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_8003521C_35E1C(s32);
f32 func_801D3018_5FE3F8(void *, f32);
void func_801F703C_62241C(void);
void func_801F72B4_622694(void *, s32, s32);
extern M2C_UNK func_801F0AD4_61BEB4;

void func_801F0414_61B7F4(void *arg0, void *arg1) {
    s32 temp_t7;

    func_801D3018_5FE3F8(arg1, 40.0f);
    func_801F72B4_622694(arg0, 0x3CA3D70A, 0x3ECCCCCD);
    if (--M2C_FIELD(arg0, s32 *, 0x7C) <= 0) {
        func_801F703C_62241C();
        func_8003521C_35E1C((s32) &func_801F0AD4_61BEB4);
    }
}
