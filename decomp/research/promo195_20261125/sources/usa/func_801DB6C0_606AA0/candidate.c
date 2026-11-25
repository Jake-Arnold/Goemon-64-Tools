typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_80034ED4_35AD4(void *);
M2C_UNK func_801D614C_60152C();

void func_801DB6C0_606AA0(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;

    func_801D614C_60152C();
    if (M2C_FIELD(arg0, s32 *, 0x80)-- == 0) {
        func_80034ED4_35AD4(arg0);
    }
}
