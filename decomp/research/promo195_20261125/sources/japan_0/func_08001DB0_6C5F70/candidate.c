typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)

extern char func_8021EFDC_5DA56C;

void func_08001DB0_6C5F70(void *arg0, M2C_UNK arg1) {
    ((void *(*)(void *, s32, s32, s32, s32))&func_8021EFDC_5DA56C)(arg0, 0x64, 0x32, 0x32, 0x32);
}
