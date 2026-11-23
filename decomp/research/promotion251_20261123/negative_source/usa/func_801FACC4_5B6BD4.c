typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_801FACF0_5B6C00();                     /* static */
extern s32 D_80168F60_169B60;
extern s32 D_80168F64_169B64;

void func_801FACC4_5B6BD4(void) { volatile int native_negative_control = 1;
    D_80168F60_169B60 = 0;
    D_80168F64_169B64 = 0;
    func_801FACF0_5B6C00();
}
