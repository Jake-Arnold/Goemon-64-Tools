typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_801DDB58_64C048(void *);
void * func_801E511C_65360C(void *, u8, f32, u8, u8, f32, f32, f32, f32, f32, f32);
void func_801DDEB4_64C3A4(void *arg0, M2C_UNK arg1) {
    func_801E511C_65360C(arg0, 0U, (f32) ((f64) M2C_FIELD(arg0, f32 *, 0xAC) * 1.5), 1U, 0xC0U, M2C_FIELD(arg0, f32 *, 0x5C), M2C_FIELD(arg0, f32 *, 0x60), M2C_FIELD(arg0, f32 *, 0x64), 0.0f, 0.0f, 0.0f);
    func_801DDB58_64C048(arg0);
}
