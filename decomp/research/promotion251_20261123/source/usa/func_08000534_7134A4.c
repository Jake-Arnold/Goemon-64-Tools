typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_0800056C_7134DC(void *, s32);
extern char func_08000978_7138E8;

void func_08000534_7134A4(void *arg0, M2C_UNK arg1) {
    func_0800056C_7134DC(arg0, M2C_FIELD(arg0, s32 *, 0xD4));
    ((M2C_UNK (*)(void *))&func_08000978_7138E8)(arg0);
}
